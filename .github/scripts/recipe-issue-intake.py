"""Trusted issue intake. Never imports, builds or executes publisher sources."""
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

MARKER = '<!-- rice-recipe-intake-v1 -->'
SHA = re.compile(r'[a-f0-9]{64}')


class IntakeError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise IntakeError('Source redirects are refused. Use committed files in the declared repository.')


def source_file(repository, commit, path, maximum):
    if not isinstance(path, str) or len(path) > 240 or not re.fullmatch(r'[A-Za-z0-9_. /-]+', path) or any(p in ('', '.', '..') for p in path.split('/')):
        raise IntakeError('Metadata contains an unsafe repository path.')
    url = 'https://raw.githubusercontent.com/' + repository + '/' + commit + '/' + urllib.parse.quote(path)
    try:
        with urllib.request.build_opener(NoRedirect).open(url, timeout=30) as response:
            value = response.read(maximum + 1)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            raise IntakeError('Missing committed file: ' + path + '. Republish with the generated marketplace metadata and media.') from None
        raise IntakeError('GitHub source download failed. Retry intake after GitHub is available.') from None
    if len(value) > maximum:
        raise IntakeError('Committed file exceeds the intake size limit: ' + path)
    return value


def section(body, heading):
    match = re.search(r'^### ' + re.escape(heading) + r'\s*\n(.*?)(?=^### |\Z)', body, re.M | re.S)
    return match.group(1).strip() if match else ''


def field(body, key):
    match = re.search(r'^' + re.escape(key) + r': ([^\r\n]+)$', body, re.M)
    return match.group(1).strip() if match else ''


def check_issue(issue, fetch=source_file):
    body = issue.get('body') or ''
    if len(body.encode()) > 65536:
        raise IntakeError('Submission text exceeds 64 KiB.')
    repository = section(body, 'Public source repository')
    if not re.fullmatch(r'https://github\.com/[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9][A-Za-z0-9._-]{0,99}', repository):
        raise IntakeError('Use one public GitHub repository URL.')
    repository = repository.removeprefix('https://github.com/')
    commit = section(body, 'Exact source commit')
    version = section(body, 'New package version')
    if not re.fullmatch(r'[a-f0-9]{40}', commit) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise IntakeError('Use an exact 40-character source commit and a release version such as 1.0.0.')
    if not re.search(r'^- \[[xX]\] ', section(body, 'Submission guidelines'), re.M):
        raise IntakeError('Confirm the submission guidelines in the issue form.')
    packaging = section(body, 'Packaging and changes')
    metadata_path = field(packaging, 'Metadata') or 'rice-marketplace.json'
    raw = fetch(repository, commit, metadata_path, 65536)
    expected_hash = field(packaging, 'Metadata SHA-256')
    expected_bytes = field(packaging, 'Metadata bytes')
    if expected_hash and (not SHA.fullmatch(expected_hash) or hashlib.sha256(raw).hexdigest() != expected_hash) or expected_bytes and expected_bytes != str(len(raw)):
        raise IntakeError('Listing metadata hash or byte count does not match the submitted commit.')
    try:
        metadata = json.loads(raw)
    except (ValueError, UnicodeError):
        raise IntakeError('Committed listing metadata is not valid JSON.') from None
    if not isinstance(metadata, dict) or metadata.get('schema') != 'ricewm.recipe-marketplace/v1' or metadata.get('version') != version:
        raise IntakeError('Committed listing metadata must use ricewm.recipe-marketplace/v1 and match this version.')
    for key, limit in [('name', 128), ('summary', 1000), ('license', 128)]:
        text = metadata.get(key)
        if not isinstance(text, str) or not text.strip() or len(text) > limit or any(ord(c) < 32 for c in text):
            raise IntakeError('Committed metadata needs a valid ' + key + '.')
    artifact = metadata.get('artifact')
    if not isinstance(artifact, dict) or artifact.get('path') != field(packaging, 'Artifact') or artifact.get('sha256') != field(packaging, 'SHA-256') or str(artifact.get('bytes')) != field(packaging, 'Bytes'):
        raise IntakeError('Committed metadata must identify the same artifact, SHA-256 and byte count as this issue.')
    if not isinstance(artifact.get('path'), str) or not artifact['path'].endswith(('.riceapp', '.rice.json', '.ricebundle')):
        raise IntakeError('Use an exported RiceWM recipe package.')
    def verify(entry, maximum):
        size = entry.get('bytes')
        if type(size) is not int or not 1 <= size <= maximum or not isinstance(entry.get('sha256'), str) or not SHA.fullmatch(entry['sha256']):
            raise IntakeError('Invalid committed file identity.')
        value = fetch(repository, commit, entry.get('path'), size)
        if len(value) != size or hashlib.sha256(value).hexdigest() != entry['sha256']:
            raise IntakeError('Committed file hash or size mismatch: ' + entry['path'])
        return value
    verify(artifact, 16 * 1024 * 1024)
    media = metadata.get('media')
    if not isinstance(media, list) or not 2 <= len(media) <= 10 or not all(isinstance(m, dict) for m in media) or sum(m.get('role') == 'icon' for m in media) != 1 or not 1 <= sum(m.get('role') == 'screenshot' for m in media) <= 8 or sum(m.get('role') == 'video-preview' for m in media) > 1:
        raise IntakeError('Include one icon and one to eight desktop screenshots in committed metadata.')
    paths = set()
    for entry in media:
        video = entry.get('role') == 'video-preview'
        if entry.get('role') not in ('icon', 'screenshot', 'video-preview') or not isinstance(entry.get('path'), str) or not entry['path'].endswith('.mp4' if video else '.webp') or entry['path'] in paths:
            raise IntakeError('Media paths must identify distinct WebP images or an MP4 preview.')
        paths.add(entry['path'])
        for key, limit in [('alt', 280), ('license', 128), ('credits', 1000)]:
            value = entry.get(key)
            if not isinstance(value, str) or not value.strip() or len(value) > limit or any(ord(c) < 32 for c in value):
                raise IntakeError('Each image needs a description, licence and credits in metadata.')
        width, height = entry.get('width'), entry.get('height')
        if type(width) is not int or type(height) is not int or not 1 <= width <= 4096 or not 1 <= height <= 4096 or entry['role'] == 'icon' and width != height:
            raise IntakeError('Images need bounded dimensions and a square icon.')
        image = verify(entry, 2 * 1024 * 1024 if video else 1024 * 1024 if entry['role'] == 'icon' else 5 * 1024 * 1024)
        if video:
            if not artifact['path'].endswith('.ricebundle') or width > 640 or height > 360 or type(entry.get('durationMillis')) is not int or not 1000 <= entry['durationMillis'] <= 30000 or type(entry.get('frameRate')) is not int or not 1 <= entry['frameRate'] <= 30 or not isinstance(entry.get('wallpaperSha256'), str) or not SHA.fullmatch(entry['wallpaperSha256']) or not any(m.get('role') == 'screenshot' and m.get('sha256') == entry.get('posterSha256') for m in media):
                raise IntakeError('Video preview must bind its packaged wallpaper and included poster with bounded timing and dimensions.')
            if len(image) < 24 or image[4:8] != b'ftyp' or not 16 <= int.from_bytes(image[:4], 'big') <= min(len(image), 4096):
                raise IntakeError('Committed preview is not an MP4 container.')
        elif len(image) < 12 or image[:4] != b'RIFF' or image[8:12] != b'WEBP' or int.from_bytes(image[4:8], 'little') != len(image) - 8:
            raise IntakeError('Committed media is not a valid WebP container: ' + entry['path'])
    return metadata


def github(path, method='GET', body=None):
    token = os.environ['GITHUB_TOKEN']
    request = urllib.request.Request('https://api.github.com/repos/' + os.environ['GITHUB_REPOSITORY'] + path, method=method,
                                    headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'},
                                    data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.build_opener(NoRedirect).open(request, timeout=30) as response:
        return json.load(response)


def feedback(number, message):
    comment = MARKER + '\n\n' + message + '\n\nNo package has been approved or published. [Intake run](https://github.com/' + os.environ['GITHUB_REPOSITORY'] + '/actions/runs/' + os.environ['GITHUB_RUN_ID'] + ').'
    # Update only our own status comment, never publisher/operator messages.
    for page in range(1, 11):
        comments = github('/issues/' + str(number) + '/comments?per_page=100&page=' + str(page))
        existing = next((c for c in comments if c.get('user', {}).get('login') == 'github-actions[bot]' and (c.get('body') or '').startswith(MARKER)), None)
        if existing:
            github('/issues/comments/' + str(existing['id']), 'PATCH', {'body': comment})
            return
        if len(comments) < 100:
            break
    github('/issues/' + str(number) + '/comments', 'POST', {'body': comment})


def qualify_issue(number):
    # OIDC authenticates this fixed trusted registry workflow. The service
    # independently verifies issue ownership and acquires all pinned source.
    # Tokens authorize transport/status only and never enter comments or logs.
    origin = 'https://ricewm.org/marketplace/api'
    oidc_url = os.environ['ACTIONS_ID_TOKEN_REQUEST_URL'] + '&audience=ricewm-marketplace-submission'
    request = urllib.request.Request(oidc_url, headers={
        'Authorization': 'Bearer ' + os.environ['ACTIONS_ID_TOKEN_REQUEST_TOKEN']})
    with urllib.request.urlopen(request, timeout=30) as response:
        token = json.load(response)['value']
    request = urllib.request.Request(origin + '/v1/marketplace/registry/issues',
        data=json.dumps({'issue': number}).encode(), method='POST', headers={
            'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token,
            'X-Rice-Source-Token': os.environ['GITHUB_TOKEN']})
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=90) as response:
            receipt = json.load(response)
    except urllib.error.HTTPError as error:
        # Only the fixed trusted service's bounded public validation message;
        # credentials, response headers and status capabilities are omitted.
        if error.code in (400, 401, 403, 413, 429):
            data = error.read(4096)
            try:
                message = json.loads(data).get('error', {}).get('message', '')
            except (ValueError, AttributeError):
                message = ''
            if isinstance(message, str) and 0 < len(message) <= 2000:
                raise IntakeError(message) from None
        raise IntakeError('Qualification intake is temporarily unavailable; the trusted workflow will need to retry.') from None
    if not re.fullmatch(r'ms_[a-f0-9]{32}', receipt.get('id', '')):
        raise IntakeError('Qualification service returned no valid submission receipt.')
    status_url = origin + '/v1/marketplace/submissions/' + receipt['id']
    feedback(number, '**Qualification queued.** The trusted service is acquiring the exact commit and running source, media, security and native workflow checks automatically. Operator approval follows successful qualification.')
    for _ in range(120):
        time.sleep(5)
        request = urllib.request.Request(status_url, headers={
            'Authorization': 'Bearer ' + receipt['statusToken']})
        with opener.open(request, timeout=30) as response:
            result = json.load(response)
        if result.get('state') in ('queued', 'running'):
            continue
        state = result.get('state', 'checks-pending')
        checks = result.get('checks', [])
        records = '\n'.join('- `' + str(item.get('id', 'check')) + '`: **' + str(item.get('status', 'pending')) + '** — ' + str(item.get('summary', '')) for item in checks)
        return '**Qualification result: ' + state + '.**\n\n' + records + '\n\nSuccessful qualification makes this exact version available for operator source/rights review and signed publication. Editing the source coordinates reruns checks; CI never approves or publishes a submission.'
    return '**Qualification is still running.** The durable job continues on the trusted service. Check the Marketplace operator queue for its results.'


def main():
    with open(os.environ['GITHUB_EVENT_PATH']) as event_file:
        event = json.load(event_file)
    number = event.get('issue', {}).get('number') or (event.get('inputs') or {}).get('issue_number')
    issues = [github('/issues/' + str(int(number)))] if number else github('/issues?state=open&per_page=100')
    for issue in issues:
        if issue.get('pull_request') or not (issue.get('title') or '').startswith(('Submit:', '[Submission]')):
            continue
        number = issue['number']
        feedback(number, '**Received — checking committed recipe metadata and media.**')
        try:
            check_issue(issue)
            message = qualify_issue(number)
        except IntakeError as error:
            message = '**Changes needed.** ' + str(error) + '\n\nPublish the corrected files, then edit this issue to use the new exact commit and generated metadata. Editing or reopening the issue reruns intake.'
        except Exception:
            message = '**Intake temporarily failed.** Source checks could not finish. Edit or reopen this issue to retry; no rejection decision was made.'
        feedback(number, message)


if __name__ == '__main__':
    main()
