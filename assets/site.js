// Kilkule · web. Progressive enhancement only: every section reads and works without this file.
(function () {
  'use strict';

  // Header border once the page scrolls.
  var nav = document.querySelector('.nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Hero diorama: the tower walks through the twelve ages. The accent follows the age, like in the game, where an age
  // only changes the accent colour. Auto-advance stops for Reduce Motion, on hover/focus and with the pause button.
  var hero = document.getElementById('hero');
  var dataNode = document.getElementById('age-data');
  if (hero && dataNode) {
    var data = JSON.parse(dataNode.textContent);
    var ages = data.ages;
    var tower = document.getElementById('tower');
    var towerImg = tower.querySelector('img');
    var nameEl = document.getElementById('age-name');
    var subEl = document.getElementById('age-sub');
    var slots = hero.querySelectorAll('[data-slot] img');
    var foes = hero.querySelectorAll('[data-foe] img');
    var toggle = hero.querySelector('[data-age="toggle"]');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    var index = 0;
    var timer = null;
    var paused = reduce.matches;
    var hovering = false;
    var STEP_MS = 3600;

    var label = hero.querySelector('.age-label');
    // Warm only the next age, so a switch never shows a half-loaded tower and nobody downloads all twelve up front.
    var warm = function (i) {
      var a = ages[(i + ages.length) % ages.length];
      [a.tower].concat(a.defenses, a.enemies).forEach(function (src) { new Image().src = data.base + src; });
    };

    // Screen readers hear the age only when the visitor changes it, never on the automatic walk.
    var show = function (next, byUser) {
      var prev = ages[index];
      index = (next + ages.length) % ages.length;
      var a = ages[index];
      hero.classList.remove('acc-' + prev.id);
      hero.classList.add('acc-' + a.id);
      towerImg.src = data.base + a.tower;
      towerImg.alt = a.stage;
      slots.forEach(function (img, i) { img.src = data.base + a.defenses[i]; img.alt = a.defenseNames[i]; });
      foes.forEach(function (img, i) { img.src = data.base + a.enemies[i]; img.alt = a.enemyNames[i]; });
      label.setAttribute('aria-live', byUser ? 'polite' : 'off');
      nameEl.textContent = a.name + ' · ' + a.stage;
      subEl.textContent = a.sub;
      if (!reduce.matches) {
        tower.classList.remove('settle');
        void tower.offsetWidth; // restart the squash-and-settle
        tower.classList.add('settle');
      }
      warm(index + 1);
    };
    var schedule = function () {
      clearInterval(timer);
      timer = null;
      if (!paused && !hovering && !document.hidden) timer = setInterval(function () { show(index + 1); }, STEP_MS);
    };
    var setPaused = function (value) {
      paused = value;
      toggle.setAttribute('aria-label', paused ? toggle.dataset.play : toggle.dataset.pause);
      toggle.classList.toggle('is-paused', paused);
      schedule();
    };

    hero.querySelectorAll('[data-age]').forEach(function (b) { b.hidden = false; });
    hero.querySelector('[data-age="prev"]').addEventListener('click', function () { show(index - 1, true); setPaused(true); });
    hero.querySelector('[data-age="next"]').addEventListener('click', function () { show(index + 1, true); setPaused(true); });
    toggle.addEventListener('click', function () { setPaused(!paused); });
    var diorama = hero.querySelector('.diorama');
    diorama.addEventListener('mouseenter', function () { hovering = true; schedule(); });
    diorama.addEventListener('mouseleave', function () { hovering = false; schedule(); });
    diorama.addEventListener('focusin', function () { hovering = true; schedule(); });
    diorama.addEventListener('focusout', function () { hovering = false; schedule(); });
    document.addEventListener('visibilitychange', schedule);
    reduce.addEventListener('change', function () { setPaused(reduce.matches || paused); });
    warm(1);
    setPaused(paused);
  }

  // Card rails: arrow buttons scroll by one card (touch and trackpad scroll natively).
  document.querySelectorAll('.rail').forEach(function (rail) {
    var bar = rail.nextElementSibling;
    if (!bar || !bar.classList.contains('rail-nav')) return;
    bar.hidden = false;
    bar.querySelectorAll('[data-rail]').forEach(function (b) {
      b.addEventListener('click', function () {
        var card = rail.firstElementChild;
        var step = card ? card.getBoundingClientRect().width + 18 : rail.clientWidth;
        rail.scrollBy({ left: step * Number(b.dataset.rail), behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      });
    });
  });
})();
