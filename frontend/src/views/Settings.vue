<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 page-fade-in">
    <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-8">设置</h1>

    <div class="space-y-6">
      <!-- 通知推送设置（仅管理员） -->
      <div v-if="authStore.isAdmin" class="bg-white dark:bg-gray-800 shadow dark:shadow-gray-700/30 sm:rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">通知推送设置</h3>

          <!-- Server酱微信推送 -->
          <div class="space-y-4 mb-6">
            <h4 class="text-md font-medium text-gray-800 dark:text-gray-200 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-2 text-green-600 dark:text-green-400">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
              </svg>
              Server酱 微信推送
            </h4>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                SendKey（多个用逗号分隔）
              </label>
              <input
                v-model="notificationSettings.serverchan_keys"
                type="text"
                placeholder="SCT123xxx,SCT456xxx"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
              <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                访问 <a href="https://sct.ftqq.com/" target="_blank" class="text-indigo-600 dark:text-indigo-400 hover:underline">sct.ftqq.com</a> 获取 SendKey
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="flex items-center">
                <input
                  id="enable-weekly"
                  v-model="notificationSettings.enable_weekly_report"
                  type="checkbox"
                  class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 dark:border-gray-600 rounded"
                />
                <label for="enable-weekly" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                  启用周报（每周一）
                </label>
              </div>

              <div v-if="notificationSettings.enable_weekly_report">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  周报发送时间
                </label>
                <input
                  v-model="notificationSettings.weekly_report_time"
                  type="time"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div class="flex items-center">
                <input
                  id="enable-monthly"
                  v-model="notificationSettings.enable_monthly_report"
                  type="checkbox"
                  class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 dark:border-gray-600 rounded"
                />
                <label for="enable-monthly" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                  启用月报（每月1号）
                </label>
              </div>

              <div v-if="notificationSettings.enable_monthly_report">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  月报发送时间
                </label>
                <input
                  v-model="notificationSettings.monthly_report_time"
                  type="time"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>
          </div>

          <!-- 邮件推送 -->
          <div class="space-y-4 border-t border-gray-200 dark:border-gray-700 pt-6">
            <h4 class="text-md font-medium text-gray-800 dark:text-gray-200 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-2 text-blue-600 dark:text-blue-400">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
              </svg>
              邮件推送
            </h4>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  SMTP 服务器
                </label>
                <input
                  v-model="notificationSettings.smtp_server"
                  type="text"
                  placeholder="smtp.qq.com"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  SMTP 端口
                </label>
                <input
                  v-model.number="notificationSettings.smtp_port"
                  type="number"
                  placeholder="465"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  发件邮箱
                </label>
                <input
                  v-model="notificationSettings.smtp_user"
                  type="email"
                  placeholder="your@email.com"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  SMTP 授权码
                </label>
                <input
                  v-model="notificationSettings.smtp_password"
                  type="password"
                  placeholder="授权码（非邮箱密码）"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                收件人（多个用逗号分隔）
              </label>
              <input
                v-model="notificationSettings.email_recipients"
                type="text"
                placeholder="user1@email.com,user2@email.com"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div class="space-y-2">
              <div class="flex items-center">
                <input
                  id="enable-email-report"
                  v-model="notificationSettings.enable_email_report"
                  type="checkbox"
                  class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 dark:border-gray-600 rounded"
                />
                <label for="enable-email-report" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                  启用邮件报表推送（周报/月报）
                </label>
              </div>

              <div class="flex items-center">
                <input
                  id="enable-transaction-notification"
                  v-model="notificationSettings.enable_transaction_notification"
                  type="checkbox"
                  class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 dark:border-gray-600 rounded"
                />
                <label for="enable-transaction-notification" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                  启用交易创建通知
                </label>
              </div>

              <div class="flex items-center">
                <input
                  id="smtp-use-tls"
                  v-model="notificationSettings.smtp_use_tls"
                  type="checkbox"
                  class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 dark:border-gray-600 rounded"
                />
                <label for="smtp-use-tls" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                  使用 TLS/SSL
                </label>
              </div>
            </div>
          </div>

          <div class="mt-6 flex items-center gap-3">
            <button
              @click="saveNotificationSettings"
              :disabled="savingNotifications"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ savingNotifications ? '保存中...' : '保存通知设置' }}
            </button>
            <p class="text-xs text-amber-600 dark:text-amber-400">
              ⚠️ 保存后部分配置需要重启服务才能生效
            </p>
          </div>
        </div>
      </div>

      <!-- 资金池设置（仅管理员） -->
      <div v-if="authStore.isAdmin" class="bg-white dark:bg-gray-800 shadow dark:shadow-gray-700/30 sm:rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">资金池设置</h3>

          <div class="space-y-4">
            <div>
              <label for="initial-amount" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                初始资金
              </label>
              <div class="relative max-w-xs">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <span class="text-gray-500 dark:text-gray-400 text-lg font-medium">¥</span>
                </div>
                <input
                  id="initial-amount"
                  v-model="formattedAmount"
                  @focus="handleFocus"
                  @blur="handleBlur"
                  type="text"
                  inputmode="decimal"
                  class="block w-full pl-10 pr-4 py-3.5 text-right text-lg font-semibold rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 apple-numbers"
                  :placeholder="formatNumber(47830.91)"
                />
              </div>
              <p class="mt-3 text-sm text-gray-500 dark:text-gray-400">
                当前初始金额：<span class="font-semibold text-gray-700 dark:text-gray-300 apple-numbers">¥{{ formatNumber(currentInitialAmount) }}</span>
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
      </div>

      <!-- 数据导出 -->
      <div class="bg-white dark:bg-gray-800 shadow dark:shadow-gray-700/30 sm:rounded-lg">
        <div class="px-4 py-5 sm:p-6">
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
import { ref, computed, onMounted } from 'vue'
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
const isFocused = ref(false)

// 通知配置
const notificationSettings = ref({
  serverchan_keys: '',
  enable_weekly_report: false,
  enable_monthly_report: false,
  weekly_report_time: '09:00',
  monthly_report_time: '09:00',
  smtp_server: '',
  smtp_port: 465,
  smtp_user: '',
  smtp_password: '',
  smtp_use_tls: true,
  email_recipients: '',
  enable_email_report: false,
  enable_transaction_notification: false,
})
const savingNotifications = ref(false)

// 格式化数字（千位分隔符）
function formatNumber(num) {
  if (num === null || num === undefined || num === '') return ''
  const number = parseFloat(num)
  if (isNaN(number)) return ''
  return number.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

// 解析格式化的数字
function parseFormattedNumber(str) {
  if (!str) return null
  // 移除千位分隔符
  const cleaned = str.replace(/,/g, '')
  const number = parseFloat(cleaned)
  return isNaN(number) ? null : number
}

// 格式化显示的金额
const formattedAmount = computed({
  get() {
    if (isFocused.value) {
      // 聚焦时显示原始数字（无格式化）
      return initialAmount.value !== null ? String(initialAmount.value) : ''
    }
    // 失焦时显示格式化数字
    return initialAmount.value !== null ? formatNumber(initialAmount.value) : ''
  },
  set(value) {
    // 移除千位分隔符并解析
    const parsed = parseFormattedNumber(value)
    initialAmount.value = parsed
  }
})

function handleFocus() {
  isFocused.value = true
}

function handleBlur() {
  isFocused.value = false
}

async function loadNotificationSettings() {
  try {
    const response = await axios.get('/api/settings/notifications')
    notificationSettings.value = response.data
  } catch (error) {
    console.error('Failed to load notification settings:', error)
  }
}

async function saveNotificationSettings() {
  savingNotifications.value = true
  try {
    await axios.put('/api/settings/notifications', notificationSettings.value)
    showMessage('通知设置已保存，部分配置需要重启服务才能生效', 'success')
  } catch (error) {
    showMessage('保存失败：' + (error.response?.data?.detail || '未知错误'), 'error')
  } finally {
    savingNotifications.value = false
  }
}

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
    loadNotificationSettings()
  }
})
</script>

<style scoped>
/* 页面淡入动画 */
.page-fade-in {
  animation: pageFadeIn 0.8s ease-out;
}

@keyframes pageFadeIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Apple 风格数字字体 */
.apple-numbers {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', system-ui, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.02em;
  font-feature-settings: 'tnum' 1;
}
</style>
