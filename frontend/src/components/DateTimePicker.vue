<template>
  <div class="relative">
    <!-- Display button -->
    <button
      type="button"
      @click.stop="isOpen = !isOpen"
      class="w-full rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 py-3 px-4 text-left text-sm font-medium text-gray-900 dark:text-white transition-all duration-200 hover:bg-gray-100 dark:hover:bg-gray-600 focus:border-indigo-500 focus:bg-white dark:focus:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 flex items-center justify-between"
    >
      <div class="flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-gray-500 dark:text-gray-400">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
        </svg>
        <span>{{ displayText }}</span>
      </div>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
           class="w-4 h-4 text-gray-500 dark:text-gray-400 transition-transform duration-200"
           :class="{'rotate-180': isOpen}">
        <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
      </svg>
    </button>

    <!-- Dropdown panel -->
    <Transition
      enter-active-class="transition duration-100 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-75 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isOpen"
        class="absolute z-50 mt-2 w-full max-h-[500px] overflow-visible rounded-2xl bg-white dark:bg-gray-800 shadow-xl dark:shadow-gray-700/30 border border-gray-200 dark:border-gray-700"
      >
        <!-- Date Selection -->
        <div class="p-4 pb-3">
          <!-- Year/Month selector -->
          <div class="flex items-center justify-between mb-3">
            <button
              type="button"
              @click.stop="prevMonth"
              class="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
              </svg>
            </button>

            <span class="text-sm font-semibold text-gray-900 dark:text-white">
              {{ currentYear }}年{{ currentMonth }}月
            </span>

            <button
              type="button"
              @click.stop="nextMonth"
              :disabled="isNextMonthDisabled"
              :class="{'opacity-30 cursor-not-allowed': isNextMonthDisabled}"
              class="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors disabled:hover:bg-transparent"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
              </svg>
            </button>
          </div>

          <!-- Calendar grid -->
          <div class="grid grid-cols-7 gap-1.5 mb-3">
            <!-- Week headers -->
            <div v-for="day in ['日', '一', '二', '三', '四', '五', '六']" :key="day"
                 class="text-center text-xs font-medium text-gray-500 dark:text-gray-400 py-1.5">
              {{ day }}
            </div>

            <!-- Calendar days -->
            <button
              v-for="day in calendarDays"
              :key="day.date"
              type="button"
              @click.stop="selectDateAndApply(day)"
              :disabled="!day.selectable"
              :class="{
                'bg-indigo-600 text-white font-semibold hover:bg-indigo-700': day.isSelected,
                'text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-600': day.isCurrentMonth && !day.isSelected && day.selectable,
                'text-gray-300 dark:text-gray-600': !day.isCurrentMonth || !day.selectable,
                'ring-2 ring-indigo-600 ring-offset-1': day.isToday && !day.isSelected,
                'cursor-not-allowed': !day.selectable
              }"
              class="h-8 text-xs rounded-lg transition-all duration-150 disabled:hover:bg-transparent flex items-center justify-center"
            >
              {{ day.day }}
            </button>
          </div>

          <!-- Today button -->
          <div class="pt-2 border-t border-gray-100 dark:border-gray-700">
            <button
              type="button"
              @click.stop="setToday"
              class="w-full rounded-lg px-4 py-2 text-sm font-medium text-indigo-600 hover:bg-indigo-50 dark:hover:bg-gray-600 transition-colors"
            >
              今天
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const currentYear = ref(new Date().getFullYear())
const currentMonth = ref(new Date().getMonth() + 1)
const selectedDate = ref(new Date())

// Initialize from modelValue
onMounted(() => {
  if (props.modelValue) {
    const date = new Date(props.modelValue)
    selectedDate.value = date
    currentYear.value = date.getFullYear()
    currentMonth.value = date.getMonth() + 1
  }
})

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    const date = new Date(newValue)
    selectedDate.value = date
    currentYear.value = date.getFullYear()
    currentMonth.value = date.getMonth() + 1
  }
})

const displayText = computed(() => {
  const date = selectedDate.value
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}年${month}月${day}日`
})

const isNextMonthDisabled = computed(() => {
  const today = new Date()
  const nextMonth = new Date(currentYear.value, currentMonth.value, 1)
  return nextMonth > today
})

const calendarDays = computed(() => {
  const days = []
  const firstDay = new Date(currentYear.value, currentMonth.value - 1, 1)
  const lastDay = new Date(currentYear.value, currentMonth.value, 0)
  const prevLastDay = new Date(currentYear.value, currentMonth.value - 1, 0)

  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const selectedDateOnly = new Date(selectedDate.value)
  selectedDateOnly.setHours(0, 0, 0, 0)

  // Previous month days
  const firstDayOfWeek = firstDay.getDay()
  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    const day = prevLastDay.getDate() - i
    const date = new Date(currentYear.value, currentMonth.value - 2, day)
    days.push({
      day,
      date: date.getTime(),
      isCurrentMonth: false,
      isToday: false,
      isSelected: false,
      selectable: false
    })
  }

  // Current month days
  for (let day = 1; day <= lastDay.getDate(); day++) {
    const date = new Date(currentYear.value, currentMonth.value - 1, day)
    const dateOnly = new Date(date)
    dateOnly.setHours(0, 0, 0, 0)

    const isToday = dateOnly.getTime() === today.getTime()
    const isSelected = dateOnly.getTime() === selectedDateOnly.getTime()
    const selectable = dateOnly <= today

    days.push({
      day,
      date: date.getTime(),
      isCurrentMonth: true,
      isToday,
      isSelected,
      selectable
    })
  }

  // Next month days to fill grid
  const remainingDays = 42 - days.length
  for (let day = 1; day <= remainingDays; day++) {
    const date = new Date(currentYear.value, currentMonth.value, day)
    days.push({
      day,
      date: date.getTime(),
      isCurrentMonth: false,
      isToday: false,
      isSelected: false,
      selectable: false
    })
  }

  return days
})

function prevMonth() {
  if (currentMonth.value === 1) {
    currentMonth.value = 12
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

function nextMonth() {
  if (isNextMonthDisabled.value) return

  if (currentMonth.value === 12) {
    currentMonth.value = 1
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

function selectDateAndApply(day) {
  if (!day.selectable) return

  const newDate = new Date(day.date)
  // Set to current time instead of 00:00 to avoid timezone issues
  const now = new Date()
  newDate.setHours(now.getHours(), now.getMinutes(), 0, 0)
  selectedDate.value = newDate

  // Emit in datetime-local format (YYYY-MM-DDTHH:mm)
  const year = newDate.getFullYear()
  const month = String(newDate.getMonth() + 1).padStart(2, '0')
  const day_str = String(newDate.getDate()).padStart(2, '0')
  const hours = String(newDate.getHours()).padStart(2, '0')
  const minutes = String(newDate.getMinutes()).padStart(2, '0')
  const formatted = `${year}-${month}-${day_str}T${hours}:${minutes}`
  emit('update:modelValue', formatted)
  isOpen.value = false
}

function setToday() {
  const now = new Date()
  selectedDate.value = now
  currentYear.value = now.getFullYear()
  currentMonth.value = now.getMonth() + 1

  // Emit in datetime-local format (YYYY-MM-DDTHH:mm) using local time
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const formatted = `${year}-${month}-${day}T${hours}:${minutes}`
  emit('update:modelValue', formatted)
  isOpen.value = false
}

// Click outside handler
function handleClickOutside(event) {
  const target = event.target
  if (!target.closest('.relative')) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
