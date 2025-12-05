<script lang="ts">
  import { onMount } from "svelte";

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

  const refresh_names = async () => {
    try {
      load_error = false;
      const response = await fetch("/api/name?count=22");
      if (!response.ok) {
        throw `HTTP ${response.status} ${response.statusText}`;
      }
      const data = await response.json();
      names = data.names;
    } catch (e) {
      console.error(`Failed to fetch names: error ${e}`);
      load_error = true;
      return;
    }
  };

  onMount(() => {
    refresh_names();
  });
</script>

<main>
  <div class="app">
    <h1>Dugnutt</h1>
    <h2>A Fighting-Baseball-inspired roster generator</h2>

    {#if load_error}
      <div class="error_bar">
        A connection error is preventing the app from generating new names right
        now
      </div>
    {/if}

    <div id="app-contents">
      {#each names as name}
        <div class="player-name">{name}</div>
      {/each}
    </div>

    <button onclick={refresh_names}>Generate New Roster</button>

    <h3>What is this?</h3>
    <div class="explanation">
      Dugnutt is a web toy inspired by the rosters from the 1994 Japanese
      baseball game
      <a href="https://en.wikipedia.org/wiki/MLBPA_Baseball">
        Fighting Baseball for the Super NES
      </a>
      . In the years since its release, it has become notorious for the mangled English
      names of the fictional players it features. (One intrepid reddit user did a
      <a
        href="https://www.reddit.com/r/baseball/comments/t1xx6g/why_bobson_and_why_dugnutt_a_deep_dive_into_why/"
      >
        deep analysis
      </a>
      of the names and discovered they were likely created by combining the names
      of contemporary MLB and NHL players from the early 90s and tweaking them slightly.)
      This toy simply generates similar-sounding names for your amusement.
    </div>

    <div class="footer">
      <div>Made by <a href="https://straythought.xyz">Adam Stone</a></div>
      <div>Link to github</div>
    </div>
  </div>
</main>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap");

  .error_bar {
    background-color: #ffaaaa;
    color: #500000;
    border-radius: 12px;
    padding: 16px;
  }

  #app-contents {
    font-family: "Press Start 2P", monospace;
    font-size: 24px;
    margin: 20px;
    padding: 20px 10px;
    background-color: #08089a;
    border-radius: 12px;
    color: white;
    text-shadow: 2px 2px 2px black;
    columns: 2;
    column-gap: 2rem;
  }

  .explanation {
    margin-top: 20px;
    font-size: 1.25em;
  }

  .footer {
    display: flex;
    justify-content: space-evenly;
    margin-top: 40px;
    font-size: 1em;
  }
</style>
