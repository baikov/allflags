/* Project specific Javascript goes here. */
$(document).ready(function () {
    // Copy color
    var cp = document.querySelectorAll('.cp');
    var clipboard = new ClipboardJS(cp);
    clipboard.on('success', function (e) {
        console.log(e);
        console.info('Action:', e.action);
        console.info('Text:', e.text);
        console.info('Trigger:', e.trigger);
        $('#copy').toast('show')
    });

    clipboard.on('error', function (e) {
        console.log(e);
    });

    // Tooltips
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

    // Accordion for FAQ and Toggle menu
    $('.collapse').collapse('hide')

    // Dropdown Bootstrap 4 menu
    $('.dropdown-menu a.dropdown-toggle').on('mouseover', function (e) {
        if (!$(this).next().hasClass('show')) {
            $(this).parents('.dropdown-menu').first().find('.show').removeClass('show');
        }
        var $subMenu = $(this).next('.dropdown-menu');
        $subMenu.toggleClass('show');


        $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function (e) {
            $('.dropdown-submenu .show').removeClass('show');
        });


        return false;
    });

    // Carousel for historical flags
    // $('.history-carousel').slick({
    //     dots: true,
    //     slidesToShow: 3,
    //     slidesToScroll: 1,
    //     autoplay: true,
    //     autoplaySpeed: 5000,
    //     responsive: [
    //         {
    //           breakpoint: 1140, // xl
    //           settings: {
    //             slidesToShow: 3,
    //             slidesToScroll: 3,
    //             infinite: true,
    //             dots: true
    //           }
    //         },
    //         {
    //           breakpoint: 960, // lg
    //           settings: {
    //             slidesToShow: 3,
    //             slidesToScroll: 2
    //           }
    //         },
    //         {
    //           breakpoint: 720, // md
    //           settings: {
    //             slidesToShow: 2,
    //             slidesToScroll: 1
    //           }
    //         },
    //         {
    //             breakpoint: 540, // sm
    //             settings: {
    //               slidesToShow: 1,
    //               slidesToScroll: 1
    //             }
    //           }
    //         // You can unslick at a given breakpoint now by adding:
    //         // settings: "unslick"
    //         // instead of a settings object
    //       ]
    // });
    // $('.history-carousel-hor').slick({
    //     dots: true,
    //     slidesToShow: 1,
    //     slidesToScroll: 1,
    //     autoplay: true,
    //     autoplaySpeed: 5000,
    // });

    $("ul.nav li a[href^='#']").on('click', function(e) {

      // prevent default anchor click behavior
      e.preventDefault();

      // store hash
      var hash = this.hash;

      if (hash == "#main") {
        var targetOffset = 0;
      }
      else {
        var targetOffset = $(hash).offset().top - 80;
      }
      // animate
      $('html, body').animate({
          scrollTop: targetOffset
        }, 1000, function(){

          // when done, add hash to url
          // (default click behaviour)
          // window.location.hash = hash;
        });

   });

});

var svgMapCountryNamesRU = {
  AF: 'Афганистан',
  AX: 'Аландские о-ва',
  AL: 'Албания',
  DZ: 'Алжир',
  AS: 'Американское Самоа',
  AD: 'Андорра',
  AO: 'Ангола',
  AI: 'Ангилья',
  AQ: 'Антарктида',
  AG: 'Антигуа и Барбуда',
  AR: 'Аргентина',
  AM: 'Армения',
  AW: 'Аруба',
  AU: 'Австралия',
  AT: 'Австрия',
  AZ: 'Азербайджан',
  BS: 'Багамы',
  BH: 'Бахрейн',
  BD: 'Бангладеш',
  BB: 'Барбадос',
  BY: 'Беларусь',
  BE: 'Бельгия',
  BZ: 'Белиз',
  BJ: 'Бенин',
  BM: 'Бермуды',
  BT: 'Бутан',
  BO: 'Боливия',
  BA: 'Босния и Герцеговина',
  BW: 'Ботсвана',
  BR: 'Бразилия',
  IO: 'Британская территория в Индийском океане',
  VG: 'Виргинские о-ва (Британские)',
  BN: 'Бруней-Даруссалам',
  BG: 'Болгария',
  BF: 'Буркина-Фасо',
  BI: 'Бурунди',
  KH: 'Камбоджа',
  CM: 'Камерун',
  CA: 'Канада',
  CV: 'Кабо-Верде',
  BQ: 'Бонэйр, Синт-Эстатиус и Саба',
  KY: 'Каймановы о-ва',
  CF: 'ЦАР',
  TD: 'Чад',
  CL: 'Чили',
  CN: 'Китай',
  CX: 'о-в Рождества',
  CC: 'Кокосовые о-ва',
  CO: 'Колумбия',
  KM: 'Коморы',
  CG: 'Конго - Браззавиль',
  CK: 'Острова Кука',
  CR: 'Коста-Рика',
  HR: 'Хорватия',
  CU: 'Куба',
  CW: 'Кюрасао',
  CY: 'Кипр',
  CZ: 'Чехия',
  CD: 'Конго - Киншаса',
  DK: 'Дания',
  DJ: 'Джибути',
  DM: 'Доминика',
  DO: 'Доминиканская Республика',
  EC: 'Эквадор',
  EG: 'Египет',
  SV: 'Сальвадор',
  GQ: 'Экваториальная Гвинея',
  ER: 'Эритрея',
  EE: 'Эстония',
  ET: 'Эфиопия',
  FK: 'Фолклендские о-ва',
  FO: 'Фарерские о-ва',
  FM: 'Федеративные Штаты Микронезии',
  FJ: 'Фиджи',
  FI: 'Финляндия',
  FR: 'Франция',
  GF: 'Французская Гвиана',
  PF: 'Французская Полинезия',
  TF: 'Французские Южные территории',
  GA: 'Габон',
  GM: 'Гамбия',
  GE: 'Грузия',
  DE: 'Германия',
  GH: 'Гана',
  GI: 'Гибралтар',
  GR: 'Греция',
  GL: 'Гренландия',
  GD: 'Гренада',
  GP: 'Гваделупа',
  GU: 'Гуам',
  GT: 'Гватемала',
  GN: 'Гвинея',
  GW: 'Гвинея-Бисау',
  GY: 'Гайана',
  HT: 'Гаити',
  HN: 'Гондурас',
  HK: 'Гонконг (специальный административный район)',
  HU: 'Венгрия',
  IS: 'Исландия',
  IN: 'Индия',
  ID: 'Индонезия',
  IR: 'Иран',
  IQ: 'Ирак',
  IE: 'Ирландия',
  IM: 'о-в Мэн',
  IL: 'Израиль',
  IT: 'Италия',
  CI: 'Кот-д’Ивуар',
  JM: 'Ямайка',
  JP: 'Япония',
  JE: 'Джерси',
  JO: 'Иордания',
  KZ: 'Казахстан',
  KE: 'Кения',
  KI: 'Кирибати',
  XK: 'Косово',
  KW: 'Кувейт',
  KG: 'Киргизия',
  LA: 'Лаос',
  LV: 'Латвия',
  LB: 'Ливан',
  LS: 'Лесото',
  LR: 'Либерия',
  LY: 'Ливия',
  LI: 'Лихтенштейн',
  LT: 'Литва',
  LU: 'Люксембург',
  MO: 'Макао (специальный административный район)',
  MK: 'Македония',
  MG: 'Мадагаскар',
  MW: 'Малави',
  MY: 'Малайзия',
  MV: 'Мальдивы',
  ML: 'Мали',
  MT: 'Мальта',
  MH: 'Маршалловы Острова',
  MQ: 'Мартиника',
  MR: 'Мавритания',
  MU: 'Маврикий',
  YT: 'Майотта',
  MX: 'Мексика',
  MD: 'Молдова',
  MC: 'Монако',
  MN: 'Монголия',
  ME: 'Черногория',
  MS: 'Монтсеррат',
  MA: 'Марокко',
  MZ: 'Мозамбик',
  MM: 'Мьянма (Бирма)',
  NA: 'Намибия',
  NR: 'Науру',
  NP: 'Непал',
  NL: 'Нидерланды',
  NC: 'Новая Каледония',
  NZ: 'Новая Зеландия',
  NI: 'Никарагуа',
  NE: 'Нигер',
  NG: 'Нигерия',
  NU: 'Ниуэ',
  NF: 'о-в Норфолк',
  KP: 'КНДР',
  MP: 'Северные Марианские о-ва',
  NO: 'Норвегия',
  OM: 'Оман',
  PK: 'Пакистан',
  PW: 'Палау',
  PS: 'Палестинские территории',
  PA: 'Панама',
  PG: 'Папуа – Новая Гвинея',
  PY: 'Парагвай',
  PE: 'Перу',
  PH: 'Филиппины',
  PN: 'острова Питкэрн',
  PL: 'Польша',
  PT: 'Португалия',
  PR: 'Пуэрто-Рико',
  QA: 'Катар',
  RE: 'Реюньон',
  RO: 'Румыния',
  RU: 'Россия',
  RW: 'Руанда',
  SH: 'о-в Св. Елены',
  KN: 'Сент-Китс и Невис',
  LC: 'Сент-Люсия',
  PM: 'Сен-Пьер и Микелон',
  VC: 'Сент-Винсент и Гренадины',
  WS: 'Самоа',
  SM: 'Сан-Марино',
  ST: 'Сан-Томе и Принсипи',
  SA: 'Саудовская Аравия',
  SN: 'Сенегал',
  RS: 'Сербия',
  SC: 'Сейшельские Острова',
  SL: 'Сьерра-Леоне',
  SG: 'Сингапур',
  SX: 'Синт-Мартен',
  SK: 'Словакия',
  SI: 'Словения',
  SB: 'Соломоновы Острова',
  SO: 'Сомали',
  ZA: 'ЮАР',
  GS: 'Южная Георгия и Южные Сандвичевы о-ва',
  KR: 'Республика Корея',
  SS: 'Южный Судан',
  ES: 'Испания',
  LK: 'Шри-Ланка',
  SD: 'Судан',
  SR: 'Суринам',
  SJ: 'Шпицберген и Ян-Майен',
  SZ: 'Свазиленд',
  SE: 'Швеция',
  CH: 'Швейцария',
  SY: 'Сирия',
  TW: 'Тайвань',
  TJ: 'Таджикистан',
  TZ: 'Танзания',
  TH: 'Таиланд',
  TL: 'Восточный Тимор',
  TG: 'Того',
  TK: 'Токелау',
  TO: 'Тонга',
  TT: 'Тринидад и Тобаго',
  TN: 'Тунис',
  TR: 'Турция',
  TM: 'Туркменистан',
  TC: 'о-ва Тёркс и Кайкос',
  TV: 'Тувалу',
  UG: 'Уганда',
  UA: 'Украина',
  AE: 'ОАЭ',
  GB: 'Великобритания',
  US: 'Соединенные Штаты',
  UM: 'Внешние малые о-ва (США)',
  VI: 'Виргинские о-ва (США)',
  UY: 'Уругвай',
  UZ: 'Узбекистан',
  VU: 'Вануату',
  VA: 'Ватикан',
  VE: 'Венесуэла',
  VN: 'Вьетнам',
  WF: 'Уоллис и Футуна',
  EH: 'Западная Сахара',
  YE: 'Йемен',
  ZM: 'Замбия',
  ZW: 'Зимбабве'
  };

var svgMapData = {
  data: {
      area: {
      name: 'Площадь',
      format: '{0} км<sup>2</sup>',
      thousandSeparator: ' ',
      },
      population: {
      name: 'Население',
      format: '{0} чел',
      thousandSeparator: ' '
      },
      density: {
      name: 'Столица',
      format: '{0}',
      thousandSeparator: '',

      }
  },
  applyData: 'area',
  values: {

  }
}
new svgMap({
  targetElementID: 'svgMap',
  data: svgMapData,
  countryNames: svgMapCountryNamesRU,
  flagType: 'emoji',
  colorNoData: '#eeeeee',
  noDataText: '',
  mouseWheelZoomEnabled: false,
  initialZoom: 1.2,
});
