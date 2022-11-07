function verileriCek() {
  return new Promise((resolve, reject) => {
    resolve(fetch("selam.json").then((cevap) => cevap.json()));
    reject("Başarısız");
  });
}

function sortResults(prop, asc, arraySort) {
  arraySort.sort(function (a, b) {
    if (asc) {
      return a[prop] > b[prop] ? 1 : a[prop] < b[prop] ? -1 : 0;
    } else {
      return b[prop] > a[prop] ? 1 : b[prop] < a[prop] ? -1 : 0;
    }
  });
}
// let sirala = urlLinki[degerSirasi + 1]   == 1 ? true : false;

async function asynCall() {
  let urlLinki = window.location + "";
  let degerSirasi = urlLinki.indexOf("=");
  let siralanacakUrunKategorisi = "urunFiyati";
  const cevap = await verileriCek();
  alert("Analiz Edilen Ürün Sayısı " + cevap.length);
  let sirala = urlLinki[degerSirasi + 1];
  if (sirala == 1) {
    sirala = true;
  } else if (sirala == 0) {
    sirala = false;
  } else if (sirala == 2) {
    sirala = true;
    siralanacakUrunKategorisi = "degerlendirmePuani";
  } else if (sirala == 3) {
    sirala = false;
    siralanacakUrunKategorisi = "degerlendirmePuani";
  }

  sortResults(siralanacakUrunKategorisi, sirala, cevap);

  console.log("cevap", cevap);

  let tabloId = document.getElementById("tableId"); // <table id="tableId"></table>
  let tabloBody = document.createElement("tbody");
  tabloId.appendChild(tabloBody);
  let analizDizisi = [];
  for (let i = 0; i < cevap.length; i++) {
    let newFiyat = Number(cevap[i].urunFiyati);
    analizDizisi.push(newFiyat);

    let tabloTr = document.createElement("tr");
    tabloBody.id = "tBody";
    tabloTr.id = i;

    let tabloResmi = document.createElement("img");
    let tabloTd = document.createElement("td");
    tabloTd.style = "width: 15%;";

    let divtd = document.createElement("div");
    divtd.classList = "text-center";

    let degerlendirme = document.createElement("p");
    degerlendirme.classList = "text-danger";
    degerlendirme.textContent =
      "Değerlendirme Puanı : " + cevap[i].degerlendirmePuani;

    let degerlendirmeTahmini = document.createElement("p");
    degerlendirmeTahmini.classList = "text-success";
    degerlendirmeTahmini.textContent =
      "Üründen En Kötü Total Kazanç : " +
      (cevap[i].degerlendirmePuani * cevap[i].urunFiyati).toFixed() +
      " TL";

    let urununNetMarji = document.createElement("p");

    let tedarikFiyati = document.createElement("input");
    tedarikFiyati.type = "number";
    tedarikFiyati.id = "t_" + i;
    tedarikFiyati.placeholder = "Tedarikten Bulduğunuz Fiyatı Giriniz : ";
    tedarikFiyati.classList = "form-control w-50 m-auto";
    urununNetMarji.classList = "text-warning";

    let komisyon = cevap[i].urunFiyati * 0.25 + 18.5;
    urununNetMarji.textContent =
      "Ürünün Net Marjı = " +
      (cevap[i].urunFiyati - komisyon).toFixed() +
      " TL";
    let tabloTd2 = document.createElement("td");
    tabloTd2.style = "width: 15%;";
    tabloTd2.textContent = cevap[i].urunAdi + " ";

    let tabloTd3 = document.createElement("td");
    tabloTd3.style = "width: 15%;";

    let p = document.createElement("p");
    p.textContent = cevap[i].urunFiyati + " TL";

    let aHref = document.createElement("a");
    aHref.href = cevap[i].urunLinki;
    aHref.target = "_blank";

    let TotaltedarikFiyatiniHesap = document.createElement("p");
    TotaltedarikFiyatiniHesap.id = "p_" + i;
    TotaltedarikFiyatiniHesap.textContent =
      "Kar Marjı İçin Lütfen Tedarik Fiyatını Giriniz";

    //Tedarik Fiyatını Hesapla
    $(document).ready(() => {
      $("#t_" + i).keyup((e) => {
        let fiyati = e.target.value;
        if (e.keyCode == 13) {
          $("#p_" + i).removeClass("text-warning");
          $("#p_" + i).addClass("text-success");

          $("#p_" + i).text(
            (cevap[i].urunFiyati - komisyon - fiyati).toFixed(2) + " TL KAR"
          );
        }
      });
    });

    tabloResmi.src = cevap[i].urunResmi;
    tabloResmi.classList = "w-100 ml-5";
    document
      .getElementById("tBody")
      .appendChild(tabloTr)
      .appendChild(tabloTd)
      .appendChild(aHref)
      .appendChild(tabloResmi);

    document
      .getElementById(i)
      .appendChild(divtd)
      .appendChild(tabloTd2)

      .appendChild(degerlendirme)
      .appendChild(degerlendirmeTahmini)
      .appendChild(urununNetMarji)
      .appendChild(TotaltedarikFiyatiniHesap)
      .appendChild(tedarikFiyati);

    document.getElementById(i).appendChild(tabloTd3).appendChild(p);
  }

  analizDizisi.sort(function (a, b) {
    return a - b;
  });

  $("#endusukMoneyP").text(analizDizisi[0] + " TL");
  $("#enYuksekMoneyP").text(analizDizisi[cevap.length - 1] + " TL");

  let toplam = 0;
  for (let i = 0; i < cevap.length; i++) {
    // $("#" + i).click(() => window.open(cevap[i].urunLinki, "_blank"));

    if (Number(cevap[i].urunFiyati) == analizDizisi[0]) {
      document.getElementById("endusukMoneyImg").src = cevap[i].urunResmi;
      document.getElementById("endusukMoneyA").href = cevap[i].urunLinki;
    }

    if (Number(cevap[i].urunFiyati) == analizDizisi[cevap.length - 1]) {
      document.getElementById("enYuksekMoneyImg").src = cevap[i].urunResmi;
      document.getElementById("enYuksekMoneyA").href = cevap[i].urunLinki;
    }

    toplam += analizDizisi[i];
  }
  $("#ortMoneyP").text((toplam / cevap.length).toFixed(00) + " TL");
  document.getElementById("ortMoneyImg").src = "ortalama.png";
}

asynCall();
