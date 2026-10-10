import {Button,Column,Label,Message,defineApp} from '@ricewm/app';

export default defineApp({
    manifest:{id:'dev.herdr.generated.marketplace-companion',name:'Desk Companion',version:'1.0.0'},
    start(){
        const status=new Label({text:'Custom additions remain disabled until the host reviews and enables them.'});
        const about=new Button({text:'What is included?',name:'companion-about'});
        about.on(Message.ACTIVATE,()=>{status.text='This development bundle includes a small app, a GNOME panel indicator and a KDE clock widget. No upstream store listing is required.';});
        return new Column({},[new Label({text:'Desk Companion'}),status,about]);
    }
});
