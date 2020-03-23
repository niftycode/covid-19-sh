var mymap = L.map('shmap', {
    minZoom: 7,
    maxZoom: 12,
    maxBounds: [
        [55.0446228, 9.4209667],
        [53.5437641, 10.0099133],
    ],
}).setView([54.0757442, 9.9815377], 8);


L.tileLayer('https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png ', {
    subdomains: 'abc',
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, '
        + '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, '
        + 'Kontakt: xern@xern.de',
}).addTo(mymap);


function render(data)
{
    document.getElementById("timestamp").innerText = data.timestamp;
    document.getElementById("source").href = data.source;
    document.getElementById("sickSum").innerText = data.infection_sum;

    data.entries.sort((a, b) => b.sick - a.sick);

    for(var i = 0; i < data.entries.length; i++) {
        var entry = data.entries[i];

        if(entry.sick == 0)
        {
            var color = "#0180b2";
            var radius = Math.sqrt(1 * 3e6 / Math.PI);;
        }
        else
        {
            var color = "red";
            var radius = Math.sqrt(entry.sick * 3e6 / Math.PI);
        }

        L.circle([entry.lat, entry.lng], {radius: radius, color: color, fillOpacity: 0.7})
            .addTo(mymap)
            .bindPopup("<b>" + entry.name + "</b><br />Infiziert: " + entry.sick);
    }
}

fetch('data.json', {cache: "no-cache"})
    .then(res => res.json())
    .then(data => render(data));
