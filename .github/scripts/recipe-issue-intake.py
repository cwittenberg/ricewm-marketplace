"""Trusted issue intake. Never imports, builds or executes publisher sources."""
import hashlib
import json
import os
import re
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
    def verify(entry, maximum):
        size = entry.get('bytes')
        if type(size) is not int or not 1 <= size <= maximum or not SHA.fullmatch(entry.get('sha256', '')):
            raise IntakeError('Invalid committed file identity.')
        value = fetch(repository, commit, entry.get('path'), size)
        if len(value) != size or hashlib.sha256(value).hexdigest() != entry['sha256']:
            raise IntakeError('Committed file hash or size mismatch: ' + entry['path'])
        return value
    verify(artifact, 16 * 1024 * 1024)
    media = metadata.get('media')
    if not isinstance(media, list) or not 2 <= len(media) <= 9 or not all(isinstance(m, dict) for m in media) or sum(m.get('role') == 'icon' for m in media) != 1 or not 1 <= sum(m.get('role') == 'screenshot' for m in media) <= 8:
        raise IntakeError('Include one icon and one to eight desktop screenshots in committed metadata.')
    paths = set()
    for entry in media:
        if entry.get('role') not in ('icon', 'screenshot') or not isinstance(entry.get('path'), str) or not entry['path'].endswith('.webp') or entry['path'] in paths:
            raise IntakeError('Media paths must identify distinct WebP files.')
        paths.add(entry['path'])
        for key, limit in [('alt', 280), ('license', 128), ('credits', 1000)]:
            value = entry.get(key)
            if not isinstance(value, str) or not value.strip() or len(value) > limit or any(ord(c) < 32 for c in value):
                raise IntakeError('Each image needs a description, licence and credits in metadata.')
        width, height = entry.get('width'), entry.get('height')
        if type(width) is not int or type(height) is not int or not 1 <= width <= 4096 or not 1 <= height <= 4096 or entry['role'] == 'icon' and width != height:
            raise IntakeError('Images need bounded dimensions and a square icon.')
        image = verify(entry, 1024 * 1024 if entry['role'] == 'icon' else 5 * 1024 * 1024)
        if len(image) < 12 or image[:4] != b'RIFF' or image[8:12] != b'WEBP' or int.from_bytes(image[4:8], 'little') != len(image) - 8:
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
            message = '**Source review required.** The recipe file, icon, screenshots, metadata, descriptions and declared rights are present at the pinned commit, and their byte counts and SHA-256 hashes match. An operator must review the source and rights and qualify the installation profile. Image decoding/security checks are still required before approval.'
        except IntakeError as error:
            message = '**Changes needed.** ' + str(error) + '\n\nPublish the corrected files, then edit this issue to use the new exact commit and generated metadata. Editing or reopening the issue reruns intake.'
        except Exception:
            message = '**Intake temporarily failed.** Source checks could not finish. Edit or reopen this issue to retry; no rejection decision was made.'
        feedback(number, message)


if __name__ == '__main__':
    main()
