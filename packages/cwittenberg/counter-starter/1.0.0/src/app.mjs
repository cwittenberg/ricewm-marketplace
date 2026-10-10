import {Button,Column,Label,Message,defineApp} from '@ricewm/app';
export default defineApp({
  manifest:{id:'dev.herdr.generated.counter-starter',name:'Counter Starter',version:'1.0.0'},
  start({createWindow}){
    let count=0;
    const value=new Label({text:'Count: 0',name:'counter-value'});
    const add=new Button({text:'Add one',name:'counter-add',accent:true});
    const reset=new Button({text:'Reset',name:'counter-reset'});
    add.on(Message.ACTIVATE,()=>{value.text='Count: '+(++count);});
    reset.on(Message.ACTIVATE,()=>{count=0;value.text='Count: 0';});
    createWindow({title:'Counter Starter',width:360,height:220,root:new Column({},[value,add,reset])});
  }
});
