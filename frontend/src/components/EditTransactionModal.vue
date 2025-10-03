<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <!-- Background overlay with blur -->
    <div class="fixed inset-0 backdrop-blur-sm bg-gray-900/20 transition-opacity" @click="$emit('close')"></div>

    <!-- Modal panel -->
    <div class="flex min-h-full items-center justify-center p-4">
      <div class="relative w-full max-w-md transform overflow-visible rounded-2xl bg-white dark:bg-gray-800 shadow-2xl dark:shadow-gray-700/30 transition-all">
        <!-- Header -->
        <div class="border-b border-gray-100 dark:border-gray-700 px-6 py-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">编辑交易记录</h3>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="px-6 py-4">
          <!-- Type Selection -->
          <div class="mb-5">
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">类型</label>
            <div class="grid grid-cols-2 gap-2">
              <button
                type="button"
                @click="form.type = 'expense'"
                :class="{
                  'bg-red-500 text-white': form.type === 'expense',
                  'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600': form.type !== 'expense'
                }"
                class="rounded-xl py-2.5 px-4 text-sm font-medium transition-all duration-200"
              >
                支出
              </button>
              <button
                type="button"
                @click="form.type = 'income'"
                :class="{
                  'bg-green-500 text-white': form.type === 'income',
                  'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600': form.type !== 'income'
                }"
                class="rounded-xl py-2.5 px-4 text-sm font-medium transition-all duration-200"
              >
                收入
              </button>
            </div>
          </div>

          <!-- Amount -->
          <div class="mb-5">
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">金额</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-gray-400">¥</span>
              <input
                v-model.number="form.amount"
                type="number"
                step="1"
                min="0"
                required
                placeholder="0.00"
                class="w-full rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 py-3 pl-8 pr-4 text-sm font-medium text-gray-900 dark:text-white transition-all duration-200 placeholder:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-600 focus:border-indigo-500 focus:bg-white dark:focus:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
              />
            </div>
          </div>

          <!-- Category -->
          <div class="mb-5">
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">分类</label>
            <div class="grid grid-cols-4 gap-3">
              <template v-if="form.type === 'expense'">
                <button
                  v-for="category in expenseCategories"
                  :key="category.value"
                  type="button"
                  @click="form.category = category.value"
                  :class="{
                    'bg-indigo-50 border-indigo-200 text-indigo-700': form.category === category.value,
                    'bg-white dark:bg-gray-700 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300': form.category !== category.value
                  }"
                  class="flex flex-col items-center justify-center p-3 border rounded-xl transition-colors duration-150 hover:border-indigo-300 hover:scale-105"
                >
                  <component :is="category.icon" class="w-5 h-5 mb-1" />
                  <span class="text-xs font-medium">{{ category.label }}</span>
                </button>
              </template>
              <template v-if="form.type === 'income'">
                <button
                  v-for="category in incomeCategories"
                  :key="category.value"
                  type="button"
                  @click="form.category = category.value"
                  :class="{
                    'bg-green-50 border-green-200 text-green-700': form.category === category.value,
                    'bg-white dark:bg-gray-700 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300': form.category !== category.value
                  }"
                  class="flex flex-col items-center justify-center p-3 border rounded-xl transition-colors duration-150 hover:border-green-300 hover:scale-105"
                >
                  <component :is="category.icon" class="w-5 h-5 mb-1" />
                  <span class="text-xs font-medium">{{ category.label }}</span>
                </button>
              </template>
            </div>
          </div>

          <!-- Date -->
          <div class="mb-5">
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">日期</label>
            <DateTimePicker v-model="form.date" />
          </div>

          <!-- Description -->
          <div class="mb-6">
            <label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">备注</label>
            <textarea
              v-model="form.description"
              rows="2"
              maxlength="200"
              placeholder="添加备注..."
              class="w-full resize-none rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 py-3 px-4 text-sm font-medium text-gray-900 dark:text-white transition-all duration-200 placeholder:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-600 focus:border-indigo-500 focus:bg-white dark:focus:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
            />
          </div>

          <!-- Error message -->
          <div v-if="error" class="mb-4 rounded-xl bg-red-50 p-3">
            <p class="text-sm font-medium text-red-600">{{ error }}</p>
          </div>
        </form>

        <!-- Footer -->
        <div class="border-t border-gray-100 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-700/50 px-6 py-4">
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="$emit('close')"
              class="rounded-xl px-5 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-300 transition-all duration-200 hover:bg-gray-100 dark:hover:bg-gray-600"
            >
              取消
            </button>
            <button
              @click="handleSubmit"
              :disabled="loading"
              class="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition-all duration-200 hover:bg-indigo-700 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? '保存中...' : '保存' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useTransactionStore } from '@/stores/transaction'
import DateTimePicker from './DateTimePicker.vue'
import {
  Squares2X2Icon,
  TruckIcon,
  ShoppingBagIcon,
  BoltIcon,
  FilmIcon,
  HeartIcon,
  AcademicCapIcon,
  FolderIcon,
  BanknotesIcon,
  GiftIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  transaction: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'success'])
const transactionStore = useTransactionStore()

// 分类配置
const expenseCategories = [
  { value: 'food', label: '餐饮', icon: Squares2X2Icon },
  { value: 'transport', label: '交通', icon: TruckIcon },
  { value: 'shopping', label: '购物', icon: ShoppingBagIcon },
  { value: 'utilities', label: '水电', icon: BoltIcon },
  { value: 'entertainment', label: '娱乐', icon: FilmIcon },
  { value: 'medical', label: '医疗', icon: HeartIcon },
  { value: 'education', label: '教育', icon: AcademicCapIcon },
  { value: 'other', label: '其他', icon: FolderIcon }
]

const incomeCategories = [
  { value: 'salary', label: '工资', icon: BanknotesIcon },
  { value: 'bonus', label: '奖金', icon: GiftIcon },
  { value: 'other', label: '其他', icon: FolderIcon }
]

const loading = ref(false)
const error = ref('')

const form = ref({
  type: '',
  amount: 0,
  category: '',
  date: '',
  description: ''
})

onMounted(() => {
  if (props.transaction) {
    form.value = {
      type: props.transaction.type,
      amount: props.transaction.amount,
      category: props.transaction.category,
      date: new Date(props.transaction.date).toISOString().slice(0, 16),
      description: props.transaction.description || ''
    }
  }
})

// Auto-select appropriate category when type changes
watch(() => form.value.type, (newType, oldType) => {
  // Only change category if switching between income and expense
  if (oldType && newType !== oldType) {
    if (newType === 'income' && !['salary', 'bonus', 'other'].includes(form.value.category)) {
      form.value.category = 'salary'
    } else if (newType === 'expense' && !['food', 'transport', 'shopping', 'utilities', 'entertainment', 'medical', 'education', 'other'].includes(form.value.category)) {
      form.value.category = 'food'
    }
  }
})

async function handleSubmit() {
  error.value = ''

  // Validate amount
  if (!form.value.amount || form.value.amount <= 0) {
    error.value = '请输入有效的金额'
    return
  }

  loading.value = true

  // Format date to local datetime string to avoid timezone issues
  const localDate = new Date(form.value.date)
  const year = localDate.getFullYear()
  const month = String(localDate.getMonth() + 1).padStart(2, '0')
  const day = String(localDate.getDate()).padStart(2, '0')
  const hours = String(localDate.getHours()).padStart(2, '0')
  const minutes = String(localDate.getMinutes()).padStart(2, '0')
  const seconds = String(localDate.getSeconds()).padStart(2, '0')
  const formattedDate = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`

  const result = await transactionStore.updateTransaction(props.transaction.id, {
    ...form.value,
    amount: parseFloat(form.value.amount), // Ensure amount is a number
    date: formattedDate
  })

  if (result.success) {
    emit('success')
  } else {
    error.value = result.message
  }

  loading.value = false
}
</script>