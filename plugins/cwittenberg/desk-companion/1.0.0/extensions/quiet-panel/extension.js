import St from 'gi://St';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

export default class QuietPanel extends Extension {
    enable(){
        this.indicator=new PanelMenu.Button(0,'Quiet Panel',false);
        this.indicator.add_child(new St.Label({text:'Quiet ·',style_class:'system-status-icon'}));
        Main.panel.addToStatusArea(this.uuid,this.indicator);
    }
    disable(){this.indicator?.destroy();this.indicator=null;}
}
