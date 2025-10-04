<template>
  <div class="relative" ref="pickerRef">
    <!-- 胶囊按钮 - 显示当前选择的日期范围 -->
    <button
      @click="togglePicker"
      class="inline-flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-full hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all shadow-sm"
    >
      <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
      </svg>
      <span class="font-semibold text-gray-900">{{ displayText }}</span>
      <svg class="w-4 h-4 text-gray-400 transition-transform" :class="{'rotate-180': isOpen}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- 弹出层 -->
    <div v-if="isOpen" class="absolute right-0 mt-2 bg-white rounded-2xl shadow-2xl border border-gray-200 z-50 overflow-hidden" :class="showCustomPicker ? 'w-[640px]' : 'w-[380px]'">
      <!-- 当前选择提示 -->
      <div class="px-6 py-3 bg-gradient-to-r from-indigo-50 to-purple-50 border-b border-gray-200">
        <p class="text-sm text-gray-600">
          <span class="font-medium">当前：</span>
          <span class="text-indigo-600 font-semibold">{{ currentRangeText }}</span>
        </p>
      </div>

      <div class="p-6">
        <!-- 快捷选项 -->
        <div class="mb-4">
          <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">快捷选项</h3>
          <div class="grid grid-cols-2 gap-2">
            <button
              v-for="shortcut in shortcuts"
              :key="shortcut.value"
              @click.stop="selectShortcut(shortcut.value)"
              class="px-4 py-2.5 text-sm font-medium rounded-lg transition-all duration-200 border"
              :class="activeShortcut === shortcut.value
                ? 'bg-indigo-600 text-white border-indigo-600 shadow-md'
                : 'bg-white text-gray-700 border-gray-300 hover:border-indigo-400 hover:bg-indigo-50'"
            >
              {{ shortcut.label }}
            </button>
          </div>
        </div>

        <!-- 分隔线 -->
        <div class="border-t border-gray-200 my-4"></div>

        <!-- 月份选择器 -->
        <div v-if="!showCustomPicker" class="mb-4">
          <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">选择月份</h3>

          <!-- 年份选择 -->
          <div class="flex items-center justify-between mb-3">
            <button @click="prevYear" class="p-1.5 hover:bg-gray-100 rounded-lg">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
            </button>
            <span class="text-base font-bold text-gray-900">{{ currentYear }}年</span>
            <button @click="nextYear" class="p-1.5 hover:bg-gray-100 rounded-lg">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </button>
          </div>

          <!-- 月份网格 -->
          <div class="grid grid-cols-3 gap-2">
            <button
              v-for="month in 12"
              :key="month"
              @click.stop="selectMonth(month)"
              :disabled="isMonthDisabled(month)"
              class="py-3 text-sm font-medium rounded-lg transition-all duration-200 border"
              :class="isMonthDisabled(month)
                ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed'
                : isMonthSelected(month)
                  ? 'bg-indigo-600 text-white border-indigo-600 shadow-md'
                  : 'bg-white text-gray-700 border-gray-200 hover:border-indigo-400 hover:bg-indigo-50'"
            >
              {{ month }}月
            </button>
          </div>
        </div>

        <!-- 自定义日期范围 -->
        <div v-if="showCustomPicker">
          <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">自定义范围</h3>

          <!-- 双日历 -->
          <div class="flex gap-4 mb-4">
            <!-- 左侧日历 - 开始日期 -->
            <div class="flex-1">
              <div class="text-center mb-3">
                <div class="flex items-center justify-between mb-2">
                  <button @click="prevMonth('start')" class="p-1 hover:bg-gray-100 rounded">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                    </svg>
                  </button>
                  <span class="text-sm font-semibold text-gray-900">{{ formatMonthYear(startCalendarMonth) }}</span>
                  <button @click="nextMonth('start')" class="p-1 hover:bg-gray-100 rounded">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                  </button>
                </div>
              </div>
              <div class="grid grid-cols-7 gap-1">
                <div v-for="day in weekDays" :key="day" class="text-center text-xs font-medium text-gray-500 py-1">
                  {{ day }}
                </div>
                <button
                  v-for="date in getCalendarDays(startCalendarMonth)"
                  :key="date.key"
                  @click="selectDate(date, 'start')"
                  :disabled="date.disabled || !isDateSelectable(date.date, 'start')"
                  class="aspect-square text-sm rounded-lg transition-all duration-150"
                  :class="getDateClass(date, 'start')"
                >
                  {{ date.day }}
                </button>
              </div>
            </div>

            <!-- 右侧日历 - 结束日期 -->
            <div class="flex-1">
              <div class="text-center mb-3">
                <div class="flex items-center justify-between mb-2">
                  <button @click="prevMonth('end')" class="p-1 hover:bg-gray-100 rounded">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                    </svg>
                  </button>
                  <span class="text-sm font-semibold text-gray-900">{{ formatMonthYear(endCalendarMonth) }}</span>
                  <button @click="nextMonth('end')" class="p-1 hover:bg-gray-100 rounded">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                  </button>
                </div>
              </div>
              <div class="grid grid-cols-7 gap-1">
                <div v-for="day in weekDays" :key="day" class="text-center text-xs font-medium text-gray-500 py-1">
                  {{ day }}
                </div>
                <button
                  v-for="date in getCalendarDays(endCalendarMonth)"
                  :key="date.key"
                  @click="selectDate(date, 'end')"
                  :disabled="date.disabled || !isDateSelectable(date.date, 'end')"
                  class="aspect-square text-sm rounded-lg transition-all duration-150"
                  :class="getDateClass(date, 'end')"
                >
                  {{ date.day }}
                </button>
              </div>
            </div>
          </div>

          <!-- 验证提示 -->
          <div v-if="validationError" class="mb-3 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-600">{{ validationError }}</p>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex gap-3">
          <button
            v-if="!showCustomPicker"
            @click.stop="showCustomPicker = true"
            class="flex-1 px-4 py-2.5 text-sm font-medium text-indigo-600 bg-indigo-50 border border-indigo-200 rounded-lg hover:bg-indigo-100 transition-all"
          >
            自定义范围
          </button>
          <template v-else>
            <button
              @click.stop="cancelCustomPicker"
              class="flex-1 px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-all"
            >
              取消
            </button>
            <button
              @click.stop="applyCustomRange"
              :disabled="!isCustomRangeValid"
              class="flex-1 px-4 py-2.5 text-sm font-medium text-white rounded-lg transition-all shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
              :class="isCustomRangeValid ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-gray-400'"
            >
              应用
            </button>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({ start: null, end: null })
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// 状态管理
const isOpen = ref(false)
const pickerRef = ref(null)
const tempStart = ref(null)
const tempEnd = ref(null)
const activeShortcut = ref('month')
const validationError = ref('')
const showCustomPicker = ref(false)
const currentYear = ref(new Date().getFullYear())

// 日历月份状态
const startCalendarMonth = ref(new Date())
const endCalendarMonth = ref(new Date(new Date().setMonth(new Date().getMonth() + 1)))

// 星期标签
const weekDays = ['日', '一', '二', '三', '四', '五', '六']

// 快捷选项 - 简化为月/季度/年度
const shortcuts = [
  { label: '本月', value: 'month' },
  { label: '上月', value: 'lastMonth' },
  { label: '本季度', value: 'quarter' },
  { label: '今年', value: 'year' }
]

// 从 localStorage 恢复或使用默认值（本月）
onMounted(() => {
  const saved = localStorage.getItem('dateRangePicker')
  if (saved) {
    const data = JSON.parse(saved)
    tempStart.value = data.start ? new Date(data.start) : null
    tempEnd.value = data.end ? new Date(data.end) : null
    activeShortcut.value = data.shortcut || 'month'

    // 立即通知父组件恢复的日期范围
    if (tempStart.value && tempEnd.value) {
      emit('change', { start: tempStart.value, end: tempEnd.value })
    }
  } else {
    // 默认本月
    selectShortcut('month')
  }

  // 点击外部关闭
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})

// 切换弹窗
function togglePicker() {
  isOpen.value = !isOpen.value
  if (!isOpen.value) {
    showCustomPicker.value = false
  }
}

// 点击外部关闭
function handleClickOutside(event) {
  if (pickerRef.value && !pickerRef.value.contains(event.target)) {
    isOpen.value = false
    showCustomPicker.value = false
  }
}

// 键盘快捷键
function handleKeydown(event) {
  if (!isOpen.value) return

  if (event.key === 'Escape') {
    isOpen.value = false
    showCustomPicker.value = false
  }
}

// 快捷选项选择
function selectShortcut(value) {
  const today = new Date()
  today.setHours(23, 59, 59, 999) // 设置为今天结束时间
  let start, end

  switch (value) {
    case 'month':
      // 本月（截止到今天）
      start = new Date(today.getFullYear(), today.getMonth(), 1)
      end = new Date(today.getFullYear(), today.getMonth() + 1, 0)
      // 如果本月还没结束，结束日期设为今天
      if (end > today) {
        end = new Date(today)
        end.setHours(23, 59, 59, 999)
      }
      break
    case 'lastMonth':
      // 上月
      start = new Date(today.getFullYear(), today.getMonth() - 1, 1)
      end = new Date(today.getFullYear(), today.getMonth(), 0)
      break
    case 'quarter':
      // 本季度（截止到今天）
      const currentQuarter = Math.floor(today.getMonth() / 3)
      start = new Date(today.getFullYear(), currentQuarter * 3, 1)
      end = new Date(today.getFullYear(), currentQuarter * 3 + 3, 0)
      // 如果本季度还没结束，结束日期设为今天
      if (end > today) {
        end = new Date(today)
        end.setHours(23, 59, 59, 999)
      }
      break
    case 'year':
      // 今年（截止到今天）
      start = new Date(today.getFullYear(), 0, 1)
      end = new Date(today.getFullYear(), 11, 31)
      // 如果今年还没结束，结束日期设为今天
      if (end > today) {
        end = new Date(today)
        end.setHours(23, 59, 59, 999)
      }
      break
  }

  tempStart.value = start
  tempEnd.value = end
  activeShortcut.value = value
  validationError.value = ''
  showCustomPicker.value = false

  // 快捷选项立即应用并关闭
  applyRange(start, end, value)
  isOpen.value = false
}

// 年份导航
function prevYear() {
  currentYear.value--
}

function nextYear() {
  currentYear.value++
}

// 选择月份
function selectMonth(month) {
  const start = new Date(currentYear.value, month - 1, 1)
  const end = new Date(currentYear.value, month, 0)

  tempStart.value = start
  tempEnd.value = end
  activeShortcut.value = null

  applyRange(start, end, null)
  isOpen.value = false
}

// 判断月份是否选中
function isMonthSelected(month) {
  if (!tempStart.value || !tempEnd.value) return false

  return tempStart.value.getFullYear() === currentYear.value &&
         tempStart.value.getMonth() === month - 1 &&
         tempStart.value.getDate() === 1 &&
         tempEnd.value.getDate() === new Date(currentYear.value, month, 0).getDate()
}

// 判断月份是否禁用（未来的月份）
function isMonthDisabled(month) {
  const today = new Date()
  const currentYearNow = today.getFullYear()
  const currentMonthNow = today.getMonth() + 1

  // 如果年份在未来，所有月份都禁用
  if (currentYear.value > currentYearNow) {
    return true
  }

  // 如果是当前年份，禁用未来的月份
  if (currentYear.value === currentYearNow && month > currentMonthNow) {
    return true
  }

  return false
}

// 取消自定义选择器
function cancelCustomPicker() {
  showCustomPicker.value = false
  validationError.value = ''
}

// 日历月份导航
function prevMonth(calendar) {
  if (calendar === 'start') {
    startCalendarMonth.value = new Date(startCalendarMonth.value.setMonth(startCalendarMonth.value.getMonth() - 1))
  } else {
    endCalendarMonth.value = new Date(endCalendarMonth.value.setMonth(endCalendarMonth.value.getMonth() - 1))
  }
}

function nextMonth(calendar) {
  if (calendar === 'start') {
    startCalendarMonth.value = new Date(startCalendarMonth.value.setMonth(startCalendarMonth.value.getMonth() + 1))
  } else {
    endCalendarMonth.value = new Date(endCalendarMonth.value.setMonth(endCalendarMonth.value.getMonth() + 1))
  }
}

// 格式化月份年份
function formatMonthYear(date) {
  return `${date.getFullYear()}年${date.getMonth() + 1}月`
}

// 获取日历天数
function getCalendarDays(monthDate) {
  const year = monthDate.getFullYear()
  const month = monthDate.getMonth()

  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)

  const days = []

  // 填充前面的空白
  const firstDayOfWeek = firstDay.getDay()
  for (let i = 0; i < firstDayOfWeek; i++) {
    const date = new Date(year, month, 1 - firstDayOfWeek + i)
    days.push({
      day: date.getDate(),
      date: date,
      disabled: true,
      key: `empty-${i}`
    })
  }

  // 当月日期
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const date = new Date(year, month, i)
    days.push({
      day: i,
      date: date,
      disabled: false,
      key: `day-${i}`
    })
  }

  return days
}

// 选择日期
function selectDate(dateObj, type) {
  if (dateObj.disabled) return

  if (type === 'start') {
    tempStart.value = dateObj.date
  } else {
    tempEnd.value = dateObj.date
  }

  activeShortcut.value = null
  validateCustomRange()
}

// 判断日期是否可选
function isDateSelectable(date, type) {
  const today = new Date()
  today.setHours(23, 59, 59, 999)

  // 未来的日期不可选
  if (date > today) {
    return false
  }

  if (type === 'start' && tempEnd.value) {
    return date <= tempEnd.value
  } else if (type === 'end' && tempStart.value) {
    const maxEnd = new Date(tempStart.value)
    maxEnd.setMonth(maxEnd.getMonth() + 12)
    return date >= tempStart.value && date <= maxEnd && date <= today
  }
  return true
}

// 获取日期样式
function getDateClass(dateObj, type) {
  if (dateObj.disabled) {
    return 'text-gray-300 cursor-not-allowed'
  }

  const dateStr = dateObj.date.toDateString()
  const startStr = tempStart.value?.toDateString()
  const endStr = tempEnd.value?.toDateString()

  // 选中的日期
  if (dateStr === startStr || dateStr === endStr) {
    return 'bg-indigo-600 text-white font-semibold shadow-md'
  }

  // 范围内的日期
  if (tempStart.value && tempEnd.value && dateObj.date > tempStart.value && dateObj.date < tempEnd.value) {
    return 'bg-indigo-100 text-indigo-900'
  }

  // 今天
  if (dateStr === new Date().toDateString()) {
    return 'border border-indigo-400 text-indigo-600 font-medium'
  }

  // 不可选日期
  if (!isDateSelectable(dateObj.date, type)) {
    return 'text-gray-300 cursor-not-allowed'
  }

  return 'text-gray-700 hover:bg-indigo-50'
}

// 验证自定义范围
function validateCustomRange() {
  validationError.value = ''

  if (!tempStart.value || !tempEnd.value) {
    return false
  }

  if (tempStart.value > tempEnd.value) {
    validationError.value = '开始日期不能晚于结束日期'
    return false
  }

  const monthDiff = (tempEnd.value.getFullYear() - tempStart.value.getFullYear()) * 12
                    + tempEnd.value.getMonth() - tempStart.value.getMonth()

  if (monthDiff > 12) {
    validationError.value = '日期范围不能超过12个月'
    return false
  }

  return true
}

// 自定义范围是否有效
const isCustomRangeValid = computed(() => {
  return tempStart.value && tempEnd.value && validateCustomRange()
})

// 应用自定义范围
function applyCustomRange() {
  if (!isCustomRangeValid.value) return

  applyRange(tempStart.value, tempEnd.value, null)
  isOpen.value = false
  showCustomPicker.value = false
}

// 应用范围
function applyRange(start, end, shortcut) {
  const range = { start, end }

  // 保存到 localStorage
  localStorage.setItem('dateRangePicker', JSON.stringify({
    start: start.toISOString(),
    end: end.toISOString(),
    shortcut
  }))

  emit('update:modelValue', range)
  emit('change', range)
}

// 显示文本
const displayText = computed(() => {
  if (!tempStart.value || !tempEnd.value) return '选择日期范围'

  const start = tempStart.value
  const end = tempEnd.value

  // 优先根据 activeShortcut 判断（如果有的话）
  if (activeShortcut.value) {
    switch (activeShortcut.value) {
      case 'month':
      case 'lastMonth':
        return `${start.getFullYear()}年${start.getMonth() + 1}月`
      case 'quarter':
        const quarter = Math.floor(start.getMonth() / 3) + 1
        return `${start.getFullYear()}年Q${quarter}`
      case 'year':
        return `${start.getFullYear()}年`
    }
  }

  // 如果没有 activeShortcut，根据日期范围智能判断
  const startQuarter = Math.floor(start.getMonth() / 3)
  const endQuarter = Math.floor(end.getMonth() / 3)
  const quarterStartMonth = startQuarter * 3

  // 如果是整年（从1月1日开始）
  if (start.getMonth() === 0 && start.getDate() === 1 &&
      start.getFullYear() === end.getFullYear()) {
    return `${start.getFullYear()}年`
  }

  // 如果是本季度（从季度第一天开始）
  if (start.getMonth() === quarterStartMonth &&
      start.getDate() === 1 &&
      start.getFullYear() === end.getFullYear() &&
      startQuarter === endQuarter) {
    return `${start.getFullYear()}年Q${startQuarter + 1}`
  }

  // 如果是同一个月（从1号开始）
  if (start.getFullYear() === end.getFullYear() &&
      start.getMonth() === end.getMonth() &&
      start.getDate() === 1) {
    return `${start.getFullYear()}年${start.getMonth() + 1}月`
  }

  // 默认显示日期范围
  return `${formatDate(start)} – ${formatDate(end)}`
})

// 当前范围文本
const currentRangeText = computed(() => {
  if (!tempStart.value || !tempEnd.value) return '未选择'
  return `${formatDate(tempStart.value)} – ${formatDate(tempEnd.value)}`
})

// 格式化日期
function formatDate(date) {
  return `${date.getFullYear()}/${String(date.getMonth() + 1).padStart(2, '0')}/${String(date.getDate()).padStart(2, '0')}`
}
</script>
