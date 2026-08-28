<script lang="ts">
  const days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
  ];

  const today = Date.now();
  const date = new Date(today).toLocaleDateString("fi-FI");
</script>

<nav class="flex justify-center lg:justify-between">
  <div class="flex flex-col sm:flex-row">
    <!-- mobile part -->
    <div class="flex items-center">
      <div class="items-center">
        <a class="text-xl sm:text-2xl xl:text-3xl" href="#">
          <strong>Missä Lounas??</strong>
        </a>
        <p>{date}</p>
      </div>
      <ul class="menu menu-horizontal lg:hidden">
        <li>
          <details>
            <summary class="text-lg bg-primary">
              Selected day
              <!-- {{ vars.selected_day.capitalize() }} -->
            </summary>
            <ul class="z-1 bg-base-200">
              Available days
              <!-- {% for day in ['monday', "tuesday", "wednesday", "thursday", -->
              <!-- "friday", "saturday", "sunday"] %} -->
              <!-- <li><a>{{ day.capitalize() }}</a></li> -->
              <!-- {% endfor %} -->
            </ul>
          </details>
        </li>
      </ul>
    </div>

    <!-- desktop day buttons -->
    <ul class="gap-3 items-center hidden lg:flex">
      {#each days as day}
        <li>
          <!-- {% if vars.selected_day == day %} -->
          <a class="lg:text-lg" href="#">
            {day}
          </a>
          <!-- {% else %} -->
          <!-- <a class="text-base xl:text-lg" href="#"> -->
          <!-- day -->
          <!-- {{ day.capitalize() }} -->
          <!-- </a> -->
          <!-- {% endif %} -->
        </li>
      {/each}
      <!-- {% for day in ['monday', "tuesday", "wednesday", "thursday", "friday", -->
      <!-- "saturday", "sunday"] %} -->
      <!-- {% endfor %} -->
    </ul>
  </div>

  <div class="flex">
    <ul class="menu menu-vertical gap-2 md:menu-horizontal">
      <li>
        <div class="dropdown dropdown-end bg-base-300 sm:dropdown-center">
          <div
            tabindex="0"
            role="button"
            class="text-base dropdown-button md:text-lg"
          >
            city
            <!-- {{ vars.selected_city }} -->
          </div>
          <ul
            tabindex="-1"
            class="justify-between dropdown-content z-1 bg-base-200"
          >
            <!-- {% for c in vars.cities %} -->
            <li>
              <a class="text-base md:text-lg hover:bg-primary" href="#">
                selected_city
              </a>
            </li>
            <!-- {% endfor %} -->
          </ul>
        </div>
      </li>
      <li>
        <div class="dropdown dropdown-end bg-base-300 sm:dropdown-center">
          <div
            tabindex="0"
            role="button"
            class="justify-between dropdown-button text-base md:text-lg text-right"
          >
            EN
          </div>
          <ul tabindex="-1" class="dropdown-content z-1 bg-base-200">
            <!-- {% for code in ['EN','FI'] %} -->
            <li>
              <a
                href="#"
                class="text-base md:text-lg bg-primary text-primary-content hover:bg-primary hover:text-primary-content"
              >
                lang_code
              </a>
            </li>
            <!-- {% endfor %} -->
          </ul>
        </div>
      </li>
    </ul>
  </div>
</nav>
