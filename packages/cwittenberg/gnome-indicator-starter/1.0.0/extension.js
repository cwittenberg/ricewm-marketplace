import St from 'gi://St';
import GObject from 'gi://GObject';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';

const Indicator=GObject.registerClass(class Indicator extends PanelMenu.Button {
    _init(){
        super._init(0.0,"Marketplace indicator");
        this._label=new St.Label({text:"Marketplace indicator",y_align:2});
        this.add_child(this._label);
        this._item=new PopupMenu.PopupMenuItem("Activate proof");
        this._item.connect("activate",()=>{this._label.text="Activated proof";});
        this.menu.addMenuItem(this._item);
    }
});
export default class GeneratedExtension extends Extension {
    enable(){this._indicator=new Indicator();Main.panel.addToStatusArea(this.uuid,this._indicator);}
    disable(){this._indicator?.destroy();this._indicator=null;}
}
