!(function () {
  function a(a) {
    var d,
      e,
      b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
      c = "";
    for (d = 0; a > d; d += 1)
      (e = Math.random() * b.length), (e = Math.floor(e)), (c += b.charAt(e));
    return c;
  }
  function b(a, b) {
    var c = CryptoJS.enc.Utf8.parse(b),
      d = CryptoJS.enc.Utf8.parse("0102030405060708"),
      e = CryptoJS.enc.Utf8.parse(a),
      f = CryptoJS.AES.encrypt(e, c, { iv: d, mode: CryptoJS.mode.CBC });
    return f.toString();
  }
  function c(a, b, c) {
    var d, e;
    return (
      setMaxDigits(131),
      (d = new RSAKeyPair(b, "", c)),
      (e = encryptedString(d, a))
    );
  }
  function d(d, e, f, g) {
    var h = {},
      // 生成随机16位字符串
      i = a(16);
    return (
      // AES加密两次
      // d、g
      (h.encText = b(d, g)),
      (h.encText = b(h.encText, i)),
      // e、f
      (h.encSecKey = c(i, e, f)),
      h
    );
  }
  function e(a, b, d, e) {
    var f = {};
    return (f.encText = c(a + e, b, d)), f;
  }
  (window.asrsea = d), (window.ecnonasr = e);
})();
(function () {
  var c9h = NEJ.P,
    ev1x = c9h("nej.g"),
    v9m = c9h("nej.j"),
    j9a = c9h("nej.u"),
    Wx4B = c9h("nm.x.ek");
  Wx4B.emj = {
    色: "00e0b",
    流感: "509f6",
    这边: "259df",
    弱: "8642d",
    嘴唇: "bc356",
    亲: "62901",
    开心: "477df",
    呲牙: "22677",
    憨笑: "ec152",
    猫: "b5ff6",
    皱眉: "8ace6",
    幽灵: "15bb7",
    蛋糕: "b7251",
    发怒: "52b3a",
    大哭: "b17a8",
    兔子: "76aea",
    星星: "8a5aa",
    钟情: "76d2e",
    牵手: "41762",
    公鸡: "9ec4e",
    爱意: "e341f",
    禁止: "56135",
    狗: "fccf6",
    亲亲: "95280",
    叉: "104e0",
    礼物: "312ec",
    晕: "bda92",
    呆: "557c9",
    生病: "38701",
    钻石: "14af6",
    拜: "c9d05",
    怒: "c4f7f",
    示爱: "0c368",
    汗: "5b7a4",
    小鸡: "6bee2",
    痛苦: "55932",
    撇嘴: "575cc",
    惶恐: "e10b4",
    口罩: "24d81",
    吐舌: "3cfe4",
    心碎: "875d3",
    生气: "e8204",
    可爱: "7b97d",
    鬼脸: "def52",
    跳舞: "741d5",
    男孩: "46b8e",
    奸笑: "289dc",
    猪: "6935b",
    圈: "3ece0",
    便便: "462db",
    外星: "0a22b",
    圣诞: "8e7",
    流泪: "01000",
    强: "1",
    爱心: "0CoJU",
    女孩: "m6Qyw",
    惊恐: "8W8ju",
    大笑: "d",
  };
  Wx4B.md = [
    "色",
    "流感",
    "这边",
    "弱",
    "嘴唇",
    "亲",
    "开心",
    "呲牙",
    "憨笑",
    "猫",
    "皱眉",
    "幽灵",
    "蛋糕",
    "发怒",
    "大哭",
    "兔子",
    "星星",
    "钟情",
    "牵手",
    "公鸡",
    "爱意",
    "禁止",
    "狗",
    "亲亲",
    "叉",
    "礼物",
    "晕",
    "呆",
    "生病",
    "钻石",
    "拜",
    "怒",
    "示爱",
    "汗",
    "小鸡",
    "痛苦",
    "撇嘴",
    "惶恐",
    "口罩",
    "吐舌",
    "心碎",
    "生气",
    "可爱",
    "鬼脸",
    "跳舞",
    "男孩",
    "奸笑",
    "猪",
    "圈",
    "便便",
    "外星",
    "圣诞",
  ];
})();
(function () {
  var c9h = NEJ.P,
    ev1x = c9h("nej.g"),
    v9m = c9h("nej.j"),
    j9a = c9h("nej.u"),
    Wx4B = c9h("nm.x.ek"),
    l9c = c9h("nm.x");
  if (v9m.be9V.redefine) return;
  window.GEnc = true;
  var bqN1x = function (cyC4G) {
    var m9d = [];
    j9a.bf9W(cyC4G, function (cyB4F) {
      m9d.push(Wx4B.emj[cyB4F]);
    });
    return m9d.join("");
  };
  var cyz4D = v9m.be9V;
  v9m.be9V = function (X9O, e9f) {
    var i9b = {},
      e9f = NEJ.X({}, e9f),
      mv3x = X9O.indexOf("?");
    if (
      window.GEnc &&
      /(^|\.com)\/api/.test(X9O) &&
      !(e9f.headers && e9f.headers[ev1x.Ae6Y] == ev1x.Im8e) &&
      !e9f.noEnc
    ) {
      if (mv3x != -1) {
        i9b = j9a.gZ1x(X9O.substring(mv3x + 1));
        X9O = X9O.substring(0, mv3x);
      }
      if (e9f.query) {
        i9b = NEJ.X(i9b, j9a.fT1x(e9f.query) ? j9a.gZ1x(e9f.query) : e9f.query);
      }
      if (e9f.data) {
        i9b = NEJ.X(i9b, j9a.fT1x(e9f.data) ? j9a.gZ1x(e9f.data) : e9f.data);
      }
      i9b["csrf_token"] = v9m.gP1x("__csrf");
      X9O = X9O.replace("api", "weapi");
      e9f.method = "post";
      delete e9f.query;
      var bVZ8R = window.asrsea(
        JSON.stringify(i9b),
        bqN1x(["流泪", "强"]),
        bqN1x(Wx4B.md),
        bqN1x(["爱心", "女孩", "惊恐", "大笑"])
      );
      e9f.data = j9a.cs0x({
        params: bVZ8R.encText,
        encSecKey: bVZ8R.encSecKey,
      });
    }
    var cdnHost = "y.music.163.com";
    var apiHost = "interface.music.163.com";
    if (location.host === cdnHost) {
      X9O = X9O.replace(cdnHost, apiHost);
      if (X9O.match(/^\/(we)?api/)) {
        X9O = "//" + apiHost + X9O;
      }
      e9f.cookie = true;
    }
    cyz4D(X9O, e9f);
  };
  v9m.be9V.redefine = true;
})();
