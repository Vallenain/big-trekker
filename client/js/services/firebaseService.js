var angular = require('angular');
var firebase = require('firebase');

module.exports = ['$firebaseArray', '$q', 'mapManagerService', 'pointsService',
    function($firebaseArray, $q, mapManagerService, pointsService) {

        var service = {
            initFirebase: initFirebase
        };

        var config = {
            apiKey: "YOUR_APIKEY",
            authDomain: "YOUR_DOMAIN.firebaseapp.com",
            databaseURL: "https://YOUR_DOMAIN.firebaseio.com",
            projectId: "YOUR_PROJECT_ID",
            storageBucket: "YOUR_STORAGE_BUCKET.appspot.com",
            messagingSenderId: "YOUR_SENDER_ID"
        };

        var refs = null;
        var points = null;

        function initFirebase() {
            var deferred = $q.defer();
            // if the connexion is bad the could be generate an error
            // if maps is not loaded
            mapManagerService.onReady().then(function() {
                if (refs === null) {
                    firebase.initializeApp(config);

                    refs = firebase.database().ref().child('sms');
                    points = $firebaseArray(refs);

                    points.$watch(function(event) {
                        deferred.resolve(); // data loaded

                        if (event.event === 'child_added') {
                            pointsService.addPoint(event.key,
                                points.$getRecord(event.key));
                        } else if (event.event === 'child_removed') {
                            pointsService.removePoint(points.$getRecord(event.key));
                        } else if (event.event === 'child_changed') {
                            pointsService.updatePoint(event.key,
                                points.$getRecord(event.key));
                        }
                    });
                } else {
                    deferred.resolve(); // data loaded
                }
            });
            return deferred.promise;
        }

        return service;
    }
];