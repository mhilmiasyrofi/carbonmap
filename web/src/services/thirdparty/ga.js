class GoogleAnalyticsThirdParty {
  constructor() {
    window.dataLayer = window.dataLayer || [];
    function gtag(){ dataLayer.push(arguments); }
    gtag('js', new Date());

    // Permanent values should be set using
    // https://developers.google.com/analytics/devguides/collection/gtagjs/setting-values

    gtag('config', 'UA-79729918-1',
      {
        'custom_map': {
          'dimension1': 'clientType',
          'dimension2': 'colorBlindModeEnabled',
          'dimension3': 'brightModeEnabled',
          'dimension4': 'isCordova',
          'dimension5': 'isEmbedded',
          'dimension6': 'solarEnabled',
          'dimension7': 'windEnabled',
          'dimension8': 'embeddedUri',
          'dimension9': 'selectedZoneName',
        }
      }
    );
    // Remember to add
    // <script async src="https://www.googletagmanager.com/gtag/js?id=UA-79729918-1"></script>
    // in head
    this.inst = gtag;

    window.onerror = function(message, url, line, col, errObject) {
        gtag('event', 'exception', {
            description: errObject,
            fatal: true,  // set to true if the exception is fatal
        });
    };
  }

  track(event, data) {
    // In both cases, track using GA
    this.inst('event', event, data);
    if (window.isCordova) {
      if (typeof cordova.plugins === 'undefined') {
        document.addEventListener('deviceready', function() {
          // Hack
          if (event === 'pageview') {
            cordova.plugins.firebase.analytics.setCurrentScreen(data.showPageState);
          } else {
            cordova.plugins.firebase.analytics.logEvent(event, data);
          }
        }, false);
      } else {
        // Duplicated code
        if (event === 'pageview') {
          cordova.plugins.firebase.analytics.setCurrentScreen(data.showPageState);
        } else {
          cordova.plugins.firebase.analytics.logEvent(event, data);
        }
      }
    }
  }

  config() {
      // Disabled for now as this creates a double tracking warning
      // in the chrome extension
      // this.inst('config', 'UA-79729918-1', ...arguments);
  }

  timingMark(eventName) {
      // Feature detects Navigation Timing API support.
      if (window.performance) {
          // Gets the number of milliseconds since page load
          // (and rounds the result since the value must be an integer).
          const timeSincePageLoad = Math.round(performance.now());
          this.timing(eventName, timeSincePageLoad);
      }
  }

  timing(eventName, durationMs) {
      this.inst('event', 'timing_complete', {
          name: eventName,
          value: durationMs,
      });
  }

  ga(){
      this.inst(...arguments);
  }
}

module.exports = new GoogleAnalyticsThirdParty();
