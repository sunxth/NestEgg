<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <!-- Background overlay with blur -->
    <div class="fixed inset-0 backdrop-blur-sm bg-gray-900/20 transition-opacity" @click="$emit('close')"></div>

    <!-- Modal panel -->
    <div class="flex min-h-full items-center justify-center p-4">
      <div class="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-white shadow-2xl transition-all">
        <!-- Header -->
        <div class="border-b border-gray-100 px-6 py-4">
          <h3 class="text-lg font-semibold text-gray-900">添加交易记录</h3>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="px-6 py-4">
          <!-- Type Selection -->
          <div class="mb-5">
            <label class="mb-2 block text-sm font-medium text-gray-700">类型</label>
            <div class="grid grid-cols-2 gap-2">
              <button
                type="button"
                @click="form.type = 'expense'"
                :class="{
                  'bg-red-500 text-white': form.type === 'expense',
                  'bg-gray-100 text-gray-700 hover:bg-gray-200': form.type !== 'expense'
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
                  'bg-gray-100 text-gray-700 hover:bg-gray-200': form.type !== 'income'
                }"
                class="rounded-xl py-2.5 px-4 text-sm font-medium transition-all duration-200"
              >
                收入
              </button>
            </div>
          </div>

          <!-- Amount -->
          <div class="mb-5">
            <label class="mb-2 block text-sm font-medium text-gray-700">金额</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">¥</span>
              <input
                v-model.number="form.amount"
                type="number"
                step="0.01"
                required
                placeholder="0.00"
                class="w-full rounded-xl border border-gray-200 bg-gray-50 py-3 pl-8 pr-4 text-sm font-medium text-gray-900 transition-all duration-200 placeholder:text-gray-400 hover:bg-gray-100 focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
              />
            </div>
          </div>

          <!-- Category -->
          <div class="mb-5">
            <label class="mb-2 block text-sm font-medium text-gray-700">分类</label>
            <div class="relative">
              <select
                v-model="form.category"
                required
                class="w-full appearance-none rounded-xl border border-gray-200 bg-gray-50 py-3 pl-4 pr-10 text-sm font-medium text-gray-900 transition-all duration-200 hover:bg-gray-100 focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
              >
                <optgroup v-if="form.type === 'expense'" label="支出分类">
                  <option value="food">🍔 餐饮</option>
                  <option value="transport">🚗 交通</option>
                  <option value="shopping">🛍️ 购物</option>
                  <option value="utilities">💡 水电</option>
                  <option value="entertainment">🎮 娱乐</option>
                  <option value="medical">🏥 医疗</option>
                  <option value="education">📚 教育</option>
                  <option value="other">📦 其他</option>
                </optgroup>
                <optgroup v-if="form.type === 'income'" label="收入分类">
                  <option value="salary">💰 工资</option>
                  <option value="bonus">🎁 奖金</option>
                  <option value="other">📦 其他</option>
                </optgroup>
              </select>
              <svg class="pointer-events-none absolute right-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </div>
          </div>

          <!-- Date -->
          <div class="mb-5">
            <label class="mb-2 block text-sm font-medium text-gray-700">日期</label>
            <input
              v-model="form.date"
              type="datetime-local"
              required
              class="w-full rounded-xl border border-gray-200 bg-gray-50 py-3 px-4 text-sm font-medium text-gray-900 transition-all duration-200 hover:bg-gray-100 focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
            />
          </div>

          <!-- Description -->
          <div class="mb-6">
            <label class="mb-2 block text-sm font-medium text-gray-700">备注</label>
            <textarea
              v-model="form.description"
              rows="2"
              maxlength="200"
              placeholder="添加备注..."
              class="w-full resize-none rounded-xl border border-gray-200 bg-gray-50 py-3 px-4 text-sm font-medium text-gray-900 transition-all duration-200 placeholder:text-gray-400 hover:bg-gray-100 focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
            />
          </div>

          <!-- Error message -->
          <div v-if="error" class="mb-4 rounded-xl bg-red-50 p-3">
            <p class="text-sm font-medium text-red-600">{{ error }}</p>
          </div>
        </form>

        <!-- Footer -->
        <div class="border-t border-gray-100 bg-gray-50/50 px-6 py-4">
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="$emit('close')"
              class="rounded-xl px-5 py-2.5 text-sm font-medium text-gray-700 transition-all duration-200 hover:bg-gray-100"
            >
              取消
            </button>
            <button
              @click="handleSubmit"
              :disabled="loading"
              class="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition-all duration-200 hover:bg-indigo-700 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? '提交中...' : '确定' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useTransactionStore } from '@/stores/transaction'

const emit = defineEmits(['close', 'success'])
const transactionStore = useTransactionStore()

const loading = ref(false)
const error = ref('')

const form = ref({
  type: 'expense',
  amount: null,
  category: 'food',
  date: new Date().toISOString().slice(0, 16),
  description: ''
})

// Auto-select appropriate category when type changes
watch(() => form.value.type, (newType) => {
  if (newType === 'income') {
    form.value.category = 'salary'
  } else {
    form.value.category = 'food'
  }
})

async function handleSubmit() {
  error.value = ''
  loading.value = true

  const result = await transactionStore.createTransaction({
    ...form.value,
    date: new Date(form.value.date).toISOString()
  })

  if (result.success) {
    emit('success')
  } else {
    error.value = result.message
  }

  loading.value = false
}
</script>