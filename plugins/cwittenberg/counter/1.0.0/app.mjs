import {Button,Column,Label,Message,defineApp} from '@ricewm/app';

export default defineApp({
    manifest:{id:'dev.herdr.generated.marketplace-counter',name:'Little Counter',version:'1.0.0'},
    start(){
        let count=0;
        const label=new Label({text:'0',name:'counter-value'});
        const increment=new Button({text:'Add one',name:'counter-add',accent:true});
        const reset=new Button({text:'Reset',name:'counter-reset'});
        increment.on(Message.ACTIVATE,()=>{label.text=String(++count);});
        reset.on(Message.ACTIVATE,()=>{count=0;label.text='0';});
        return new Column({},[new Label({text:'A little counter. No network or file access.'}),label,increment,reset]);
    }
});
