<script lang="ts">
  import { onMount } from "svelte";
  import { slide } from "svelte/transition";
  import { flip } from "svelte/animate";
  import { quadInOut } from "svelte/easing";

  let names: string[] = $state([
    "SLEVE MCDICHAEL",
    "WILLIE DUSTICE",
    "ONSON SWEEMEY",
    "JEROMY GRIDE",
    "DARRYL ARCHIDELD",
    "SCOTT DOURQUE",
    "ANATOLI SMORIN",
    "SHOWN FURCOTTE",
    "REY MCSRIFF",
    "DEAN WESREY",
    "GLENALLEN MIXON",
    "MIKE TRUK",
    "MARIO MCRLWAIN",
    "DWIGT RORTUGAL",
    "RAUL CHAMGERLAIN",
    "TIM SANDAELE",
    "KEVIN NOGILY",
    "KARL DANDLETON",
    "TONY SMEHRIK",
    "MIKE SERNANDEZ",
    "BOBSON DUGNUTT",
    "TODD BONZALEZ",
  ]);

  let load_error: Boolean = $state(false);
  let load_waiting: Boolean = $state(false);

  const refresh_names = async () => {
    const timer = setTimeout(() => {
      load_waiting = true;
    }, 500);

    try {
      load_error = false;

      const response = await fetch(
        import.meta.env.VITE_API_URL + "/api/name?count=22",
      );
      if (!response.ok) {
        throw `HTTP ${response.status} ${response.statusText}`;
      }
      const data = await response.json();
      names = data.names;
    } catch (e) {
      console.error(`Failed to fetch names: error ${e}`);
      load_error = true;
      return;
    } finally {
      clearTimeout(timer);
      load_waiting = false;
    }
  };

  onMount(() => {
    refresh_names();
  });
</script>

<main>
  <div class="dugnutt-app">
    <h1>Dugnutt</h1>
    <h2>A Fighting-Baseball-inspired roster generator</h2>

    {#if load_error}
      <div
        class="error_bar"
        transition:slide={{
          duration: 500,
          axis: "y",
          easing: quadInOut,
        }}
      >
        A connection error is preventing the app from generating new names right
        now
      </div>
    {/if}

    {#if load_waiting}
      <div
        transition:slide={{
          duration: 500,
          axis: "y",
          easing: quadInOut,
        }}
        class="loading_bar"
      >
        <div class="spinner"></div>
        <span class="loading_text">
          Waiting for a response...this can take up to 45 seconds
        </span>
      </div>
    {/if}

    <div class="app-slide-container">
      <div class="dugnutt-app-frame">
        <div id="dugnutt-app-contents">
          {#each names as name}
            <div class="player-name">{name}</div>
          {/each}
        </div>
      </div>

      <button onclick={refresh_names}>Generate New Roster</button>

      <h3>What is this?</h3>
      <div class="explanation">
        Dugnutt is a web toy inspired by the rosters from the 1994 Japanese
        baseball game
        <a href="https://en.wikipedia.org/wiki/MLBPA_Baseball">
          Fighting Baseball for the Super NES
        </a>
        . In the years since its release, it has become notorious for the mangled
        English names of the fictional players it features. (One intrepid reddit user
        did a
        <a
          href="https://www.reddit.com/r/baseball/comments/t1xx6g/why_bobson_and_why_dugnutt_a_deep_dive_into_why/"
        >
          deep analysis
        </a>
        of the names and discovered they were likely created by combining the names
        of MLB and NHL players from the early 90s and tweaking them slightly.) This
        toy simply generates similar-sounding names for your amusement.
      </div>

      <div class="footer">
        <div>
          Made by <a href="https://straythought.xyz">Adam Stone</a>
        </div>
        <div>
          <a href="https://github.com/adam-stone/dugnutt">
            <img src="/public/img/github-mark.svg" alt="github" height="20" />
            <span>Source code</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</main>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap");

  .dugnutt-app .error_bar {
    background-color: #ffaaaa;
    color: #500000;
    border-radius: 12px;
    padding: 16px;
  }

  .dugnutt-app .loading_bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    background-color: #f7f3a8;
    color: #8f4a0a;
    border-radius: 12px;
    padding: 16px;
  }

  .dugnutt-app .loading_bar .spinner {
    width: 20px;
    height: 20px;
    border: 2px solid #a2a8b0;
    border-top-color: #44546b;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .dugnutt-app .app-slide-container {
    transition: transform 0.5s ease-in-out;
  }

  .dugnutt-app-frame {
    margin: 20px;
    padding: 20px 10px;
    background-color: #08089a;
    border-radius: 12px;
    color: white;
    overflow-x: auto;
  }

  #dugnutt-app-contents {
    margin: 0;
    padding: 0;
    font-family: "Press Start 2P", monospace;
    font-size: 18px;
    text-shadow: 2px 2px 2px black;
    min-width: 640px;
  }

  @media (min-width: 1024px) {
    #dugnutt-app-contents {
      columns: 2;
      column-gap: 2rem;
    }
  }

  @media (min-width: 512px) {
    #dugnutt-app-contents {
      font-size: 24px;
    }
  }
  .dugnutt-app .explanation {
    margin-top: 20px;
    font-size: 1.25em;
  }

  .dugnutt-app .footer {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    margin-top: 40px;
    font-size: 1em;
  }

  .dugnutt-app .footer div img,
  .dugnutt-app .footer div span {
    margin: 0;
    display: inline;
    vertical-align: middle;
  }

  .dugnutt-app button {
    border-radius: 8px;
    border: 1px solid transparent;
    padding: 0.6em 1.2em;
    font-size: 1em;
    font-weight: 600;
    font-family: inherit;
    background: linear-gradient(170deg, #c03030 0%, #c08010 100%);
    color: white;
    cursor: pointer;
    transition:
      transform 0.2s,
      box-shadow 0.2s;
  }

  .dugnutt-app button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  .dugnutt-app button:focus,
  .dugnutt-app button:focus-visible {
    outline: 4px auto -webkit-focus-ring-color;
  }
</style>
