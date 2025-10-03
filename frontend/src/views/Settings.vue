<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-8">设置</h1>

    <div class="bg-white dark:bg-gray-800 shadow dark:shadow-gray-700/30 sm:rounded-lg">
      <!-- 资金池设置（仅管理员） -->
      <div v-if="authStore.isAdmin" class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">资金池设置</h3>

        <div class="space-y-4">
          <div>
            <label for="initial-amount" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              初始资金
            </label>
            <div class="mt-1 flex rounded-md shadow-sm">
              <span class="inline-flex items-center px-3 rounded-l-md border border-r-0 border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-500 dark:text-gray-400 sm:text-sm">
                ¥
              </span>
              <input
                id="initial-amount"
                v-model.number="initialAmount"
                type="number"
                step="0.01"
                class="flex-1 block w-full px-3 py-2 rounded-none rounded-r-md border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="47830.00"
              />
            </div>
            <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
              设置资金池的初始金额，当前：¥{{ currentInitialAmount.toFixed(2) }}
            </p>
          </div>

          <div>
            <button
              @click="showResetConfirm = true"
              :disabled="!initialAmount"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              重置资金池
            </button>
            <p class="mt-2 text-sm text-red-600">
              ⚠️ 警告：重置将删除所有交易记录，且无法恢复！
            </p>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-200 dark:border-gray-700 px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">数据导出</h3>

        <div class="space-y-4">
          <div>
            <button
              @click="exportCSV"
              class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
            >
              导出 CSV 文件
            </button>
            <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
              将所有交易记录导出为 CSV 格式文件
            </p>
          </div>

          <div>
            <button
              @click="exportDatabase"
              class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
            >
              备份数据库
            </button>
            <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
              下载完整的 SQLite 数据库文件作为备份
            </p>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-200 dark:border-gray-700 px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">系统信息</h3>

        <dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
          <div>
            <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">当前用户</dt>
            <dd class="mt-1 text-sm text-gray-900 dark:text-white">
              {{ authStore.isAdmin ? '管理员' : '普通用户' }}
            </dd>
          </div>

          <div>
            <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">权限说明</dt>
            <dd class="mt-1 text-sm text-gray-900 dark:text-white">
              {{ authStore.isAdmin ? '可以添加、编辑、删除记录' : '仅可查看记录' }}
            </dd>
          </div>

          <div>
            <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">版本</dt>
            <dd class="mt-1 text-sm text-gray-900 dark:text-white">v1.0.0</dd>
          </div>

          <div>
            <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">最后登录</dt>
            <dd class="mt-1 text-sm text-gray-900 dark:text-white">{{ new Date().toLocaleString() }}</dd>
          </div>
        </dl>
      </div>

      <div class="border-t border-gray-200 dark:border-gray-700 px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">帮助</h3>

        <div class="prose prose-sm text-gray-500 dark:text-gray-400">
          <p>NestEgg 是一个简单的家庭记账系统，帮助您轻松管理家庭财务。</p>
          <ul>
            <li>管理员可以添加、编辑和删除交易记录</li>
            <li>普通用户可以查看所有记录和统计信息</li>
            <li>支持按类型、分类、日期筛选记录</li>
            <li>提供月度和分类统计图表</li>
            <li>支持数据导出和备份</li>
          </ul>
        </div>
      </div>
    </div>

    <div v-if="message" class="mt-4 rounded-md p-4"
         :class="message.type === 'success' ? 'bg-green-50 dark:bg-green-900/30' : 'bg-red-50 dark:bg-red-900/30'">
      <p class="text-sm"
         :class="message.type === 'success' ? 'text-green-800 dark:text-green-200' : 'text-red-800 dark:text-red-200'">
        {{ message.text }}
      </p>
    </div>

    <!-- 重置确认对话框 -->
    <div v-if="showResetConfirm" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex min-h-screen items-center justify-center p-4">
        <div class="fixed inset-0 bg-gray-900/75 backdrop-blur-sm transition-opacity" @click="showResetConfirm = false"></div>

        <div class="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-gray-800 shadow-2xl dark:shadow-gray-700/30 transition-all">
          <div class="p-6">
            <div class="flex items-center gap-4 mb-4">
              <div class="flex-shrink-0 w-12 h-12 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
                <svg class="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">确认重置资金池</h3>
                <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">此操作不可撤销</p>
              </div>
            </div>

            <div class="mb-6">
              <div class="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-4">
                <p class="text-sm font-medium text-red-800 dark:text-red-200 mb-2">⚠️ 警告：以下操作将被执行</p>
                <ul class="text-sm text-red-700 dark:text-red-300 space-y-1 list-disc list-inside">
                  <li>删除所有交易记录</li>
                  <li>重置初始资金为：¥{{ initialAmount?.toFixed(2) || '0.00' }}</li>
                  <li>资金池余额将重置为初始金额</li>
                  <li><strong>此操作无法恢复</strong></li>
                </ul>
              </div>

              <p class="text-sm text-gray-600 dark:text-gray-300">
                请输入 <strong class="text-red-600 dark:text-red-400">RESET</strong> 以确认此操作：
              </p>
              <input
                v-model="confirmText"
                type="text"
                placeholder="输入 RESET 确认"
                class="mt-2 w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
              />
            </div>

            <div class="flex gap-3">
              <button
                @click="showResetConfirm = false; confirmText = ''"
                class="flex-1 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
              >
                取消
              </button>
              <button
                @click="resetFundPool"
                :disabled="confirmText !== 'RESET' || resetting"
                class="flex-1 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {{ resetting ? '重置中...' : '确认重置' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTransactionStore } from '@/stores/transaction'
import axios from '@/utils/axios'

const authStore = useAuthStore()
const transactionStore = useTransactionStore()

const message = ref(null)
const initialAmount = ref(null)
const currentInitialAmount = ref(47830)
const showResetConfirm = ref(false)
const confirmText = ref('')
const resetting = ref(false)

async function exportCSV() {
  const result = await transactionStore.exportCSV()
  if (result.success) {
    showMessage('CSV 文件已下载', 'success')
  } else {
    showMessage(result.message, 'error')
  }
}

async function exportDatabase() {
  try {
    const response = await axios.get('/api/export/database', {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `nestegg_backup_${new Date().toISOString().split('T')[0]}.db`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    showMessage('数据库备份已下载', 'success')
  } catch (error) {
    showMessage('备份失败', 'error')
  }
}

function showMessage(text, type) {
  message.value = { text, type }
  setTimeout(() => {
    message.value = null
  }, 3000)
}

async function loadFundPool() {
  try {
    const response = await axios.get('/api/fund-pool/')
    currentInitialAmount.value = parseFloat(response.data.initial_amount)
    initialAmount.value = currentInitialAmount.value
  } catch (error) {
    console.error('Failed to load fund pool:', error)
  }
}

async function resetFundPool() {
  if (confirmText.value !== 'RESET') {
    return
  }

  resetting.value = true

  try {
    // 1. 删除所有交易记录
    const transactions = await axios.get('/api/transactions/')
    for (const transaction of transactions.data) {
      await axios.delete(`/api/transactions/${transaction.id}`)
    }

    // 2. 重置资金池
    await axios.put('/api/fund-pool/reset', {
      initial_amount: initialAmount.value
    })

    showMessage('资金池已成功重置', 'success')
    showResetConfirm.value = false
    confirmText.value = ''

    // 等待一下让用户看到成功消息，然后刷新页面
    setTimeout(() => {
      window.location.reload()
    }, 1500)
  } catch (error) {
    showMessage('重置失败：' + (error.response?.data?.detail || '未知错误'), 'error')
  } finally {
    resetting.value = false
  }
}

onMounted(() => {
  if (authStore.isAdmin) {
    loadFundPool()
  }
})
</script>