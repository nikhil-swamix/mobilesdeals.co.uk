<script>
	import DistinctDropdown from './DistinctDropdown.svelte';
</script>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
	<div class="container">
		<a class="navbar-brand" href="/">Mobiles Deals UK - Ultimate Deals </a>
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>

		<DistinctDropdown label="Merchants" faIconClass="fas fa-shop" qAttribute="merchant_name" />
		<DistinctDropdown label="Networks" faIconClass="fa-duotone fa-diagram-project" qAttribute="Telcos:network" />
		<DistinctDropdown label="Brands" faIconClass="fas fa-bolt" qAttribute="brand_name" />
		<DistinctDropdown label="Sims" faIconClass="fa-duotone fa-sim-cards" qAttribute="Telcos:network?Telcos:device_product_json.product_type=SIM%20Card" />
		<div class="collapse navbar-collapse" id="navbarNav">
			<ul class="navbar-nav ml-auto">
				<!-- <li class="nav-item active">
					<a class="nav-link" href="#"><i class="fas fa-mobile-alt"></i> Mobile Phones <span class="sr-only">(current)</span></a>
				</li> -->
				<!-- <li class="nav-item">
					<a class="nav-link" href="#sim"><i class="fas fa-sim-card"></i> SIM Only</a>
				</li> -->
				<li class="nav-item">
					<a class="nav-link" href="#"><i class="fas fa-question-circle"></i> Help</a>
				</li>
			</ul>
		</div>
	</div>
</nav>

<slot />

<footer class="bg-dark text-white text-center p-3">
	<p>MobilesDeals.co.uk All rights reserved &copy; 2023</p>
</footer>
