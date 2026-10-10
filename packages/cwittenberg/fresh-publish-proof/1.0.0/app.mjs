import {Button,Column,Label,Message,defineApp} from '@ricewm/app';
export default defineApp({
  manifest:{"id":"dev.herdr.generated.fresh-publish-proof","name":"Fresh source proof","version":"1.0.0"},
  start(){
    const label=new Label({text:'Ready'});
    const button=new Button({text:'Say hello',accent:true});
    button.on(Message.ACTIVATE,()=>{label.text='Hello from your RiceApp';});
    return new Column({},[label,button]);
  }
});
