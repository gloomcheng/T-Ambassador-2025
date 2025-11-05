// 不同層級的連結設定(功能頁前的頁面連結)
//路徑跟關卡等可以增減的按鈕連結在新增按鈕時即可設定連結，所以這裡沒有。

var userProfile="user_profile.html";//使用者資料的頁面
var functions="function.html";//功能頁面
var road="road.html";//讓使用者選擇路徑的頁面
var manual="manual.html";//使用說明頁面(可以依需求設計成故事楔子頁面)
var teach="teach.html";//詳細使用教學頁面

//api引用位址
// 動態 API baseUrl 設定：本地測試用 localhost，Cloudflare Tunnel 用 window.location.origin

// 動態 API baseUrl 設定：本地優先、github.io 走 tdance.fansee.studio、其他走 window.location.origin
let apiBaseUrl;
if (location.hostname.endsWith('github.io')) {
	apiBaseUrl = 'https://tdance.fansee.studio/trips/api/';
} else if (
	location.hostname === 'localhost' ||
	location.hostname === '127.0.0.1' ||
	location.hostname.endsWith('trycloudflare.com')
	) {
	// 本地或 Cloudflare Tunnel 皆走本地 API
	apiBaseUrl = window.location.origin + '/api/';
} else {
	apiBaseUrl = 'https://tdance.fansee.studio/api/';
}
console.log('API baseUrl:', apiBaseUrl);
var postDetailUrl = apiBaseUrl + 'post-detail/'; // 通關狀況讀取(arScan.js)
var questionUrl   = apiBaseUrl + 'question/';    // 問題資料讀取(arScan.js)
var postUrl       = apiBaseUrl + 'post/';        // 通關狀況資料表更新(arScan.js)
var userUrl       = apiBaseUrl + 'user/';        // 使用者資料表新增(userProfile.js)
var marketQuestionsUrl = apiBaseUrl + 'market-questions/'; // 市集隨機題目
var marketListUrl = apiBaseUrl + 'markets/'; // 市集清單
