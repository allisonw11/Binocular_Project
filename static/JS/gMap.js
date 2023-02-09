'use strict';

function initMap() {
    const eventCoord = {
        lat: 37.768009,
        lng: -122.387787,
    };

    const basicMap = new google.maps.Map(document.querySelector('#map'), {
        center: eventCoord,
        zoom:11,
    });

    const eventMarker = new google.maps.Marker({
        position: eventCoord,
        title: 'Center',
        map: basicMap,
    });

    const eventInfo = new google.maps.InfoWindow({
        content: '<h3>Event Title Here!</h3>',
    });

    eventInfo.open(basicMap, eventMarker);
}
