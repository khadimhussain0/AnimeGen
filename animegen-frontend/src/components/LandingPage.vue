<template>
  <div>
    <!-- Header Section -->
    <header>
      <nav>
        <div class="logo">LLM AI</div>
        <ul>
          <li><a href="#features">Features</a></li>
          <li><a href="#how-it-works">How it Works</a></li>
          <li><a href="#benefits">Benefits</a></li>
          <li><a href="#pricing">Pricing</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </nav>
    </header>
    <!-- Get Started Section -->
    <section id="get-started" class="get-started">
      <h2>Get Started Today</h2>
      <p>Join the AI revolution and elevate your business to new heights. Sign up now to unleash the full potential of LLM AI.</p>
      <router-link to="/auth" class="cta-button">Sign Up Now</router-link>
    </section>

    <!-- Footer Section -->
    <footer>
      <section id="contact" class="contact">
        <h2>Contact Us</h2>
        <p>Have questions or need assistance? Reach out to us!</p>
        <a href="mailto:info@llmai.com">info@llmai.com</a>
      </section>

      <div class="social-icons">
        <a href="#" target="_blank"><img src="../assets/twitter-icon.png" alt="Twitter"></a>
        <a href="#" target="_blank"><img src="../assets/linkedin-icon.png" alt="LinkedIn"></a>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  methods: {
    redirectToCreateAccount() {
      this.$router.push('/auth');
    },
  },
};
</script>

<style scoped>
/* Global Styles */
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
}

/* Header Styles */
header {
  background-color: #292b2c;
  color: #ffffff;
  padding: 1rem;
  text-align: center;
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
}

ul {
  list-style: none;
  display: flex;
}

li {
  margin: 0 1rem;
}

a {
  text-decoration: none;
  color: #ffffff;
}

/* Hero Styles */
.hero {
  background-color: #343a40;
  color: #ffffff;
  text-align: center;
  padding: 3rem 0;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
}

p {
  font-size: 1.2rem;
  margin-top: 1rem;
}

.cta-button {
  display: inline-block;
  background-color: #007bff;
  color: #ffffff;
  padding: 0.5rem 1rem;
  text-decoration: none;
  font-size: 1rem;
  margin-top: 1rem;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background-color: #0056b3;
}


h2 {
  font-size: 1.5rem;
}

h3 {
  font-size: 1.2rem;
}

/* Get Started Section Styles */
.get-started {
  text-align: center;
  margin: 3rem 0;
}

/* Footer Styles */
footer {
  background-color: #f8f9fa;
  padding: 3rem 0;
}

.contact {
  text-align: center;
}

.social-icons {
  margin-top: 1.5rem;
}

.social-icons a {
  margin: 0 1rem;
}

.social-icons img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}
</style>
