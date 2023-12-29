<div class="row mt-3">
		<!-- color selector -->
		<div class="col">
			<div class="list-group">
				<a href="#" class="list-group-item text-center list-group-item-action active bg-dark border-black bg-gradient fw-bold" aria-current="true">
					<i class="fas fa-paint-brush"></i>
					SELECT COLOR
				</a>
				<div class="list-group-item">
					<div class="row justify-content-center py-2 g-1">
						{#key [selections['Telcos:network'], selections.brand_name]}
							{#if selections.colour}
								<!-- show single -->
								<button class="col-lg-auto col-auto btn mx-1 px-1 btn shadow-sm btn-dark bg-gradient" on:click={() => (selections.colour = selections.colour)}>
									<!-- fa -->
									<i class="fas fa-circle fa-lg" style="color: {colormap[selections.colour]};" />
									{selections.colour}
								</button>
							{:else}
								<!-- else content here -->
								{#await getDistinctColours() then value}
									{#each value as colour}
										<button class="col-lg-auto col-auto btn mx-1 px-1 btn shadow-sm btn-dark bg-gradient" on:click={() => (selections.colour = colour)}>
											<!-- fa -->
											<i class="fas fa-circle fa-lg" style="color: {colormap[colour]};" />
											{colour}
										</button>
									{/each}
								{/await}
							{/if}
						{/key}
					</div>
				</div>
			</div>
		</div>
		<!-- size delector -->
		<div class="col">
			<div class="list-group">
				<a href="#" class="list-group-item text-center list-group-item-action active bg-dark border-black bg-gradient fw-bold" aria-current="true">
					<i class="fa-duotone fa-boxes-packing"></i>
					SELECT SIZE
				</a>
				<div class="list-group-item">
					<div class="row justify-content-center py-2 g-1">
						{#key [selections['Telcos:network'], selections.brand_name]}
							{#if selections['Telcos:storage_size']}
								<!-- show single -->
								<button
									class="col-lg-auto col-auto btn mx-1 px-1 btn shadow-sm btn-dark bg-gradient"
									on:click={() => (selections['Telcos:storage_size'] = selections['Telcos:storage_size'])}
								>
									<!-- fa -->

									{selections['Telcos:storage_size']}
								</button>
							{:else}
								<!-- else content here -->
								{#await getDistinctSizes() then value}
									{#each value as size}
										<button class="col-lg-auto col-auto btn mx-1 px-1 btn shadow-sm btn-dark bg-gradient" on:click={() => (selections['Telcos:storage_size'] = size)}>
											<!-- fa -->

											{size}
										</button>
									{/each}
								{/await}
							{/if}
						{/key}
					</div>
				</div>
			</div>
		</div>
	</div>