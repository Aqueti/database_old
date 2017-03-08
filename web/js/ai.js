/*************************************************************
 * ai.js
 *
 * krpano interface functions
 *************************************************************/
"use strict";

var AI = function()
{
   this.interactive = null;

   this.init = function( panoid, interact )
   {
      this.id = panoid;
      this.pano = document.getElementById(this.id);

      //set interactive

      if( interact != false)
      {
         this.setInteractive("false");
      }
      else
      {
         this.setInteractive("true");
      }
   }

   /*************************************************************
    * dblClickFunction
    *************************************************************/
    this.dblClick = function() 
    {
       if( !this.interactive)
          return;

       //Get position
       var mpos = this.getMouse(this.pano);
   
       var view={};
       view["h"]=mpos["ath"];
       view["v"]=mpos["atv"];
   
       //Move to new position
       view['fov']= this.pano.get("view.fov")*.8;
   
       this.setView( view, 1);
    }
   
   
   /*************************************************************
    * getPosition
    *************************************************************/
   this.getView = function ()
   {
      var pos={};
       pos['h'] = this.pano.get("view.hlookat");
       pos['v'] = this.pano.get("view.vlookat");
       pos['fov']  = this.pano.get("view.fov");

       return pos;  
   }
   
   /*************************************************************
    * setView
    *************************************************************/
   this.setView = function( pos, speed)
   {
      if( speed == null )
         speed = 10;
      this.pano.call("lookto("+pos["h"]+","+pos["v"]+","+pos["fov"]+",smooth("+speed+","+(-speed)+","+speed+"));");
   /*
      this.pano.set( "view.hlookat", pos["h"]);
      this.pano.set( "view.vlookat", pos["v"]);
   */
   }
   
   
   /*************************************************************
    * getPosition
    *************************************************************/
   this.getMouse = function()
   {
      var mouse={};
   
   	this.pano.call("screentosphere(mouse.x, mouse.y, mouse.ath, mouse.atv)");
   
      mouse['x'] = this.pano.get("mouse.x");
      mouse['y'] = this.pano.get("mouse.y");
      mouse['ath'] = this.pano.get("mouse.ath");
      mouse['atv'] = this.pano.get("mouse.atv");
   
      return mouse;  
   }
   
   /*************************************************************
    * setInteractive
    *************************************************************/
   this.setInteractive = function( state )
   {
      if( state )
      {
         this.pano.set("control.usercontrol","all");
         this.interactive = true;
      }
      else
      {
         this.pano.set("control.usercontrol","none");
         this.interactive = false;
      }
   }
};

/*************************************************************
 * initialization function
 *************************************************************/
function init(panoid)
{
   var ai = new AI(panoid);

   return ai;
}

