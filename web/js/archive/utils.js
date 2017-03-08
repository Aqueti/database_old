module.exports = {
/************************************************************
 * isArray
 ************************************************************/
  isArray: function ( obj ) 
  {
          return isObject(obj) && (obj instanceof Array);
  },

  /************************************************************
   * isObject 
   ************************************************************/
  isObject: function ( obj ) 
  {
             return obj && (typeof obj  === "object");
  }
};

