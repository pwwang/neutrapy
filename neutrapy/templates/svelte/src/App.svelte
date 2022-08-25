<script>
  import GenRandom from './lib/GenRandom.svelte'

</script>

<main>
  <h1>Generate a random number each time with Python at backend</h1>
  <code>
    <pre>>>> from random import randint
>>> print(randint(0, 100))
</pre>
  </code>
  <br />
  <GenRandom />
</main>

<style>
h1 {
  font-size: 2rem;
}
pre {
    background-color: lightgray;
    border-radius: .5rem;
    font-size: .9rem;
    text-align: left;
    padding: 0 1rem;
    margin: 1rem auto;
    width: 80%;
}
</style>
