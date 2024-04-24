<script>
export let activeSelection
</script>

<div class="radio-container">
<label>
	<input type=radio bind:group={activeSelection} name="selector" value={'age'}>
	AGE
</label>

<label>
	<input type=radio bind:group={activeSelection} name="selector" value={'race'}>
	RACE
</label>

<label>
	<input type=radio bind:group={activeSelection} name="selector" value={'gender'}>
	GENDER
</label>

<label>
	<input type=radio bind:group={activeSelection} name="selector" value={'income'}>
	INCOME
</label>

<label>
	<input type=radio bind:group={activeSelection} name="selector" value={'cars per household'}>
	CARS PER HOUSEHOLD
</label>

<label>
	<input type=radio bind:group={activeSelection} name="selector" value={'mode of transit/work commute'}>
	MODE OF TRANSIT/WORK COMMUTE
</label>
</div>

<style>
	.radio-container {
		position: fixed;
		top: 16px;
		left: 16px;
		background-color: white;
		padding: 4px;
		border-radius: 2px;
	}
</style>