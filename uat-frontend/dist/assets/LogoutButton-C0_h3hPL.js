import{_ as r,u as d,c as a,o as n,n as l,t as i,s as c}from"./index-C7sBCj21.js";const m={name:"LogoutButton",props:{buttonText:{type:String,default:"Logout"},showIcon:{type:Boolean,default:!0},showText:{type:Boolean,default:!0},size:{type:String,default:"normal",validator:t=>["small","normal","large"].includes(t)},theme:{type:String,default:"admin",validator:t=>["admin","tester"].includes(t)}},setup(){const t=d();return{handleLogout:()=>{t.logout()}}}},g={key:0,class:"fas fa-sign-out-alt"},h={key:1};function _(t,o,e,s,f,y){return n(),a("button",{onClick:o[0]||(o[0]=(...u)=>s.handleLogout&&s.handleLogout(...u)),class:c(["logout-btn",[{small:e.size==="small"},`theme-${e.theme}`]])},[e.showIcon?(n(),a("i",g)):l("",!0),e.showText?(n(),a("span",h,i(e.buttonText),1)):l("",!0)],2)}const p=r(m,[["render",_],["__scopeId","data-v-143310e1"]]);export{p as L};
