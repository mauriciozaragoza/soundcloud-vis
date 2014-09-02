angular.module('SoundApp', [
	'SoundApp.controllers'
]).config(function($sceProvider) {
  // Completely disable SCE.  For demonstration purposes only!
  // Do not use in new projects.
  $sceProvider.enabled(false);
});