!function(n){function o(e){if(t[e])return t[e].exports;var r=t[e]={i:e,l:!1,exports:{}};return n[e].call(r.exports,r,r.exports,o),r.l=!0,r.exports}var t={};o.m=n,o.c=t,o.d=function(n,t,e){o.o(n,t)||Object.defineProperty(n,t,{configurable:!1,enumerable:!0,get:e})},o.n=function(n){var t=n&&n.__esModule?function(){return n.default}:function(){return n};return o.d(t,"a",t),t},o.o=function(n,o){return Object.prototype.hasOwnProperty.call(n,o)},o.p="",o(o.s=0)}([function(n,o){$(function(){$("form.subscribe .submit").click(function(){$(this).parent("form").submit()}),$(".navbar a").click(function(n){n.stopPropagation()}),$(".navbar").click(function(){$("html,body").animate({scrollTop:$("html, body").offset().top},200)});var n=new RegExp(/^[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/i);if($('footer form input[type="email"]').keyup(function(){n.test($(this).val())?$("footer form").addClass("valid"):$("footer form").removeClass("valid")}),null==new MobileDetect(window.navigator.userAgent).mobile()){var o=$(".hero i"),t=$(".devfest-banner"),e=($("nav"),$(".hero")),r=function(n){return"translate3d(0px, -"+n+"px, 0px)"},i=function(){var n=$(window).scrollTop(),n=Math.min(n,o.height());o.css({transform:r(.333333*n),"-o-transform":r(.333333*n),"-moz-transform":r(.333333*n),"-webkit-transform":r(.333333*n)}),void 0!==t&&(n>e.height()?t.addClass("up"):n<=0&&t.removeClass("up"))};$(window).on("scroll",function(){window.requestAnimationFrame(i)}),$(window).on("resize",function(){window.requestAnimationFrame(i)}),window.requestAnimationFrame(i)}})}]);