'use strict';
const map_lat = document.querySelector("#map_lat").value;
const map_lng = document.querySelector("#map_lng").value;


function initMap() {
    const eventCoord = {
        lat: Number(map_lat),
        lng: Number(map_lng),
    };

    const basicMap = new google.maps.Map(document.querySelector('#map'), {
        center: eventCoord,
        zoom:15,
    });

    const eventMarker = new google.maps.Marker({
        position: eventCoord,
        title: 'Center',
        map: basicMap,
    });

    
    const eventInfo = new google.maps.InfoWindow({
        content: 'Here',
    });

    eventInfo.open(basicMap, eventMarker);
};
