// 不同層級的連結設定(功能頁前的頁面連結)
//路徑跟關卡等可以增減的按鈕連結在新增按鈕時即可設定連結，所以這裡沒有。

var userProfile="user_profile.html";//使用者資料的頁面
var functions="function.html";//功能頁面
var road="road.html";//讓使用者選擇路徑的頁面
var manual="manual.html";//使用說明頁面(可以依需求設計成故事楔子頁面)
var teach="teach.html";//詳細使用教學頁面

//api引用位址
var postDetailUrl = "https://tdance.fansee.studio/trips/api/post-detail/";//通關狀況讀取(arScan.js)
var questionUrl = "https://tdance.fansee.studio/trips/api/question/";//問題資料讀取(arScan.js)
var postUrl = "https://tdance.fansee.studio/trips/api/post/";//通關狀況資料表更新(arScan.js)
var userUrl = "https://tdance.fansee.studio/trips/api/user/";//使用者資料表新增(userProfile.js)
