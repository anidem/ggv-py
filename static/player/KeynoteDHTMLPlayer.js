var kDeviceUnknown = "deviceUnknown";
var kDeviceDesktop = "deviceDesktop";
var kDeviceMobile = "deviceMobile";
var kModeUnknown = "modeUnknown";
var kModeDesktop = "modeDesktop";
var kModeMobile = "modeMobile";
var kBrowserUnknown = "browserUnknown";
var kBrowserDesktopSafari = "browserDesktopSafari";
var kBrowserMobileSafari = "browserMobileSafari";
var kOrientationUnknown = "orientationUnknown";
var kOrientationLandscape = "orientationLandscape";
var kOrientationPortrait = "orientationPortrait";
var kShowModeHyperlinksOnly = 2;
var kSoundTrackModePlayOnce = 0;
var kSoundTrackModeLooping = 1;
var kSoundTrackModeOff = 2;
var kOpacityPropertyName = "opacity";
var kVisibilityPropertyName = "visibility";
var kZIndexPropertyName = "z-index";
var kDisplayPropertyName = "display";
var kDisplayBlockPropertyValue = "block";
var kDisplayNonePropertyValue = "none";
var kTransformOriginTopLeftPropertyValue = "top left";
var kTransformOriginCenterPropertyValue = "center";
var kTransformStylePreserve3DPropertyValue = "preserve-3d";
var kTransformStyleFlatPropertyValue = "flat";
var kPositionAbsolutePropertyValue = "absolute";
var kPositionRelativePropertyValue = "relative";
var kBackfaceVisibilityHiddenPropertyValue = "hidden";
var kiPhoneDeviceWidth = 320;
var kiPhoneDeviceHeight = 480;
var kiPhoneLandscapeButtonBarHeight = 32;
var kiPhonePortraitButtonBarHeight = 44;
var kiPhoneUrlBarHeight = 60;
var kiPhoneStatusBarHeight = 20;
var kiPadDeviceWidth = 768;
var kiPadDeviceHeight = 1024;
var kiPadLandscapeButtonBarHeight = 32;
var kiPadPortraitButtonBarHeight = 44;
var kiPadUrlBarHeight = 0;
var kiPadStatusBarHeight = 0;
var kiPadAddressBarHeight = 30;
var kiPadBookmarksBarHeight = 30;
var kiPadMaxMoviesPerScene = 20;
var kMaxSceneDownloadWaitTime = 15000;
var kMaxScriptDownloadWaitTime = 20000;
var kWaitingIndicatorFadeOutDuration = 2000;
var kHideAddressBarDelay = 3000;
var kSceneLoadPollInterval = 100;
var kSceneLoadDisplaySpinnerTime = 3000;
var kSceneLoadDisplaySpinnerPollCount = kSceneLoadDisplaySpinnerTime / kSceneLoadPollInterval;
var kSceneLoadGiveUpTime = 60000;
var kSceneLoadGiveUpPollCount = kSceneLoadGiveUpTime / kSceneLoadPollInterval;
var kPropertyName_currentSlide = "currentSlide";
var kKeyCode_Plus = 107;
var kKeyCode_Minus = 109;
var kKeyCode_Dot = 110;
var kKeyCode_F11 = 122;
var kKeyCode_F12 = 123;
var kKeyCode_Hyphen = 189;
var kKeyCode_Equal = 187;
var kKeyCode_Period = 190;
var kKeyCode_Slash = 191;
var kKeyCode_Space = 32;
var kKeyCode_Escape = 27;
var kKeyCode_LeftArrow = 37;
var kKeyCode_UpArrow = 38;
var kKeyCode_RightArrow = 39;
var kKeyCode_DownArrow = 40;
var kKeyCode_OpenBracket = 219;
var kKeyCode_CloseBracket = 221;
var kKeyCode_Home = 36;
var kKeyCode_End = 35;
var kKeyCode_PageUp = 33;
var kKeyCode_PageDown = 34;
var kKeyCode_Return = 13;
var kKeyCode_N = 78;
var kKeyCode_P = 80;
var kKeyCode_Q = 81;
var kKeyCode_S = 83;
var kKeyCode_Delete = 8;
var kKeyCode_0 = 48;
var kKeyCode_9 = 57;
var kKeyCode_Numeric_0 = 96;
var kKeyCode_Numeric_9 = 105;
var kKeyModifier_Shift = 1000;
var kKeyModifier_Ctrl = 2000;
var kKeyModifier_Alt = 3000;
var kKeyModifier_Meta = 4000;
var kHelpPlacardMainTitle = CoreDocs.loc("Keyboard Shortcuts", "Keyboard Shortcuts");
var kHelpPlacardNavigationTitle = CoreDocs.loc("Navigation", "Navigation");
var kHelpPlacardOtherTitle = CoreDocs.loc("Other", "Other");
var kHelpPlacardAdvanceToNextBuild = CoreDocs.loc("Advance to next build", "Advance to next build");
var kHelpPlacardGoBackToPreviousBuild = CoreDocs.loc("Go back to previous build", "Go back to previous build");
var kHelpPlacardAdvanceToNextSlide = CoreDocs.loc("Advance to next slide", "Advance to next slide");
var kHelpPlacardGoBackToPreviousSlide = CoreDocs.loc("Go back to previous slide", "Go back to previous slide");
var kHelpPlacardGoToFirstSlide = CoreDocs.loc("Go to first slide", "Go to first slide");
var kHelpPlacardGoToLastSlide = CoreDocs.loc("Go to last slide", "Go to last slide");
var kHelpPlacardQuitPresentationMode = CoreDocs.loc("Quit presentation mode", "Quit presentation mode");
var kHelpPlacardGoToSpecificSlide = CoreDocs.loc("Go to specific slide", "Go to specific slide");
var kHelpPlacardShowOrHideKeyboardShortcuts = CoreDocs.loc("Show or hide Keyboard Shortcuts", "Show or hide Keyboard Shortcuts");
var kHelpPlacardShowOrHideTheCurrentSlideNumber = CoreDocs.loc("Show or hide the current slide number", "Show or hide the current slide number");
var kUnableToReachiWorkTryAgain = CoreDocs.loc("Slide couldn't be displayed.\nDo you want to try again?", "alert text to display when we timeout trying to download resources from iWork.com");
var kSlideLabel = CoreDocs.loc("Slide", "Prefix label for 'Slide I/N' display");
var kTapOrSwipeToAdvance = CoreDocs.loc("Tap or Swipe to advance", "Help string for bottom of portrait mode on mobile device");
var kOSUnknown = "unknown";
var kOSWindows = "Windows";
var kOSMacOSX = "Mac OS X";
var kOSiOS = "iOS";
var gTheoreticalMaxPixelCount = 1024 * 1024 * 3;
var gSafeMaxPixelCount = gTheoreticalMaxPixelCount * 0.9;
var gShowController = null;
var gDevice = kDeviceUnknown;
var gBrowser = kBrowserUnknown;
var gMode = kModeUnknown;
var gIpad = false;
var gOS = kOSUnknown;
var browserPrefix, browserVersion;
var userAgentString = window.navigator.userAgent;
var isMacOS = window.navigator.platform.indexOf("Mac") !== -1;
var isChrome = userAgentString.lastIndexOf("Chrome/") > 0;

if (Prototype.Browser.WebKit) {
    browserPrefix = "webkit"
} else {
    if (Prototype.Browser.Gecko) {
        var isIE = userAgentString.lastIndexOf("Trident/") > 0;
        if (isIE) {
            var revisionStringIE = userAgentString.substring(userAgentString.lastIndexOf("rv"), userAgentString.lastIndexOf(")"));
            var revisionIE = [];
            if (revisionStringIE.lastIndexOf(":") > 0) {
                revisionIE = revisionStringIE.split(":");
                browserVersion = parseFloat(revisionIE[1])
            } else {
                if (revisionStringIE.lastIndexOf(" ") > 0) {
                    revisionIE = revisionStringIE.split(" ");
                    browserVersion = parseFloat(revisionIE[1])
                } else {
                    browserVersion = 11
                }
            }
            browserPrefix = "ms"
        } else {
            browserPrefix = "moz"
        }
    } else {
        if (Prototype.Browser.IE) {
            browserPrefix = "ms";
            browserVersion = parseFloat(navigator.appVersion.split("MSIE")[1])
        }
    }
}
var kKeyframesPropertyName = "@-" + browserPrefix + "-keyframes";
var kAnimationNamePropertyName = "-" + browserPrefix + "-animation-name";
var kAnimationDurationPropertyName = "-" + browserPrefix + "-animation-duration";
var kAnimationDelayPropertyName = "-" + browserPrefix + "-animation-delay";
var kAnimationFillModePropertyName = "-" + browserPrefix + "-animation-fill-mode";
var kAnimationTimingFunctionPropertyName = "-" + browserPrefix + "-animation-timing-function";
var kAnimationIterationCountPropertyName = "-" + browserPrefix + "-animation-iteration-count";
var kTransformPropertyName = "-" + browserPrefix + "-transform";
var kTransformOriginPropertyName = "-" + browserPrefix + "-transform-origin";
var kTransformOriginZPropertyName = "-" + browserPrefix + "-transform-origin-z";
var kTransitionPropertyName = "-" + browserPrefix + "-transition-property";
var kTransitionDurationName = "-" + browserPrefix + "-transition-duration";
var kTransformStylePropertyName = "-" + browserPrefix + "-transform-style";
var kTransitionPropertyName = "-" + browserPrefix + "-transition";
var kTransitionEndEventName = browserPrefix + "TransitionEnd";
var kAnimationEndEventName = browserPrefix + "AnimationEnd";
var kPerspectivePropertyName = "-" + browserPrefix + "-perspective";
var kPerspectiveOriginPropertyName = "-" + browserPrefix + "-perspective-origin";
var kBackfaceVisibilityPropertyName = "-" + browserPrefix + "-backface-visibility";
var kBoxShadowPropertyName = "-" + browserPrefix + "-box-shadow";
var kBorderPropertyName = "border";
var kBackgroundImagePropertyName = "background-image";
var kFullscreenChangeEventName = browserPrefix + "fullscreenchange";
if (window.attachEvent) {
    window.attachEvent("onload", setupShowController)
} else {
    if (window.addEventListener) {
        window.addEventListener("load", setupShowController, false)
    } else {
        document.addEventListener("load", setupShowController, false)
    }
}

function static_url(a) {
    return a
}

function setupShowController() {
    var a = isMobileSafari();
    if (a) {
        gBrowser = kBrowserMobileSafari;
        gDevice = kDeviceMobile;
        gMode = kModeMobile;
        gIpad = isiPad()
    } else {
        gBrowser = kBrowserDesktopSafari;
        gDevice = kDeviceDesktop;
        gMode = kModeDesktop
    }
    debugMessage(kDebugSetupShowController, "================================================================================");
    debugMessage(kDebugSetupShowController, "===                     S T A R T   O F   S E S S I O N                      ===");
    debugMessage(kDebugSetupShowController, "================================================================================");
    debugMessage(kDebugSetupShowController, "userAgent: " + navigator.userAgent);
    debugMessage(kDebugSetupShowController, "url: " + window.location.href);
    if (navigator.userAgent.match(/Windows/)) {
        gOS = kOSWindows
    }
    var b = getUrlParameter("pixelLimit");
    if (b != "") {
        gSafeMaxPixelCount = 1024 * 1024 * parseInt(b)
    }
    if (navigator.userAgent.indexOf("deviceDesktop") != -1) {
        debugMessage(kDebugSetupShowController, "Device was '" + gDevice + "', overriding device to be 'deviceDesktop'");
        gDevice = kDeviceDesktop
    }
    if (navigator.userAgent.indexOf("deviceMobile") != -1) {
        debugMessage(kDebugSetupShowController, "Device was '" + gDevice + "', overriding device to be 'deviceMobile'");
        gDevice = kDeviceMobile
    }
    if (navigator.userAgent.indexOf("modeDesktop") != -1) {
        debugMessage(kDebugSetupShowController, "Mode was '" + gMode + "', overriding device to be 'modeDesktop'");
        gMode = kModeDesktop
    }
    if (navigator.userAgent.indexOf("modeMobile") != -1) {
        debugMessage(kDebugSetupShowController, "Mode was '" + gMode + "', overriding device to be 'modeMobile'");
        gMode = kModeMobile
    }
    debugMessage(kDebugSetupShowController, "  gDevice: " + gDevice);
    debugMessage(kDebugSetupShowController, " gBrowser: " + gBrowser);
    debugMessage(kDebugSetupShowController, "    gMode: " + gMode);
    debugMessage(kDebugSetupShowController, "                     gOS: " + gOS);
    gShowController = new ShowController();
    gShowController.displayManager.showWaitingIndicator();
    gShowController.delegate.setPlaybackReadyHandler(function() {
        gShowController.startShow()
    })
}

function extractDelegateFromUrlParameter() {
    var d = getUrlParameter("delegate");
    var a;
    if ((d == "") || (d == null) || (typeof(d) == "undefined")) {
        a = new NullDelegate()
    } else {
        var c = d.indexOf(".");
        a = window;
        while (c != -1) {
            var b = d.substring(0, c);
            a = a[b];
            d = d.substring(c + 1);
            c = d.indexOf(".")
        }
        a = a[d]
    }
    return a
}
var NullDelegate = Class.create({
    initialize: function() {},
    showDidLoad: function() {},
    showExited: function() {
        history.go(-1)
    },
    propertyChanged: function(b, a) {},
    setPlaybackReadyHandler: function(a) {
        a()
    }
});