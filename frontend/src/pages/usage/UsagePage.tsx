import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { useUsage } from '@/hooks/useApi'
import { DollarSign, FileText, Search, Zap } from 'lucide-react'

export function UsagePage() {
  const { data: usageStats, isLoading } = useUsage()

  if (isLoading) {
    return <UsageSkeleton />
  }

  if (!usageStats) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold">Usage Data Unavailable</h1>
        <p className="text-muted-foreground mt-2">
          Unable to load your usage statistics at this time.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Usage Analytics</h1>
        <p className="text-muted-foreground">
          Track your COGENT usage and costs
        </p>
      </div>

      {/* Overview Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Cost</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${usageStats.totalCost.toFixed(2)}
            </div>
            <p className="text-xs text-muted-foreground">
              All time usage
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Tokens</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {usageStats.totalTokens.toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              Processed tokens
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Documents Generated</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {usageStats.documentsGenerated}
            </div>
            <p className="text-xs text-muted-foreground">
              Total documents
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Searches Performed</CardTitle>
            <Search className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {usageStats.searchesPerformed}
            </div>
            <p className="text-xs text-muted-foreground">
              Total searches
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Daily Usage */}
      <Card>
        <CardHeader>
          <CardTitle>Daily Usage (Last 30 Days)</CardTitle>
          <CardDescription>
            Track your daily token consumption and costs
          </CardDescription>
        </CardHeader>
        <CardContent>
          {usageStats.dailyUsage && usageStats.dailyUsage.length > 0 ? (
            <div className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <h4 className="text-sm font-medium mb-2">Recent Days</h4>
                  <div className="space-y-2">
                    {usageStats.dailyUsage.slice(-7).map((day) => (
                      <div key={day.date} className="flex justify-between items-center py-2 border-b">
                        <span className="text-sm">
                          {new Date(day.date).toLocaleDateString('en-US', { 
                            month: 'short', 
                            day: 'numeric' 
                          })}
                        </span>
                        <div className="text-right">
                          <div className="text-sm font-medium">
                            ${day.cost.toFixed(2)}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            {day.tokens.toLocaleString()} tokens
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h4 className="text-sm font-medium mb-2">Usage Summary</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Average daily cost</span>
                      <span className="text-sm font-medium">
                        ${(usageStats.dailyUsage.reduce((sum, day) => sum + day.cost, 0) / usageStats.dailyUsage.length).toFixed(2)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Average daily tokens</span>
                      <span className="text-sm font-medium">
                        {Math.round(usageStats.dailyUsage.reduce((sum, day) => sum + day.tokens, 0) / usageStats.dailyUsage.length).toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Peak daily cost</span>
                      <span className="text-sm font-medium">
                        ${Math.max(...usageStats.dailyUsage.map(day => day.cost)).toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-8">
              <Zap className="mx-auto h-12 w-12 text-muted-foreground" />
              <h3 className="mt-2 text-sm font-semibold">No usage data</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                Start using COGENT to see your usage analytics here
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Billing Info */}
      <Card>
        <CardHeader>
          <CardTitle>Billing Information</CardTitle>
          <CardDescription>
            Usage-based pricing and payment details
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <h4 className="text-sm font-medium mb-2">Current Month</h4>
                <div className="text-2xl font-bold">
                  ${usageStats.totalCost.toFixed(2)}
                </div>
                <p className="text-sm text-muted-foreground">
                  Estimated charges for current billing period
                </p>
              </div>
              
              <div>
                <h4 className="text-sm font-medium mb-2">Pricing</h4>
                <div className="text-sm space-y-1">
                  <div className="flex justify-between">
                    <span>OpenRouter API calls</span>
                    <span>Usage + margin</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Document generation</span>
                    <span>Per 1K tokens</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Search queries</span>
                    <span>Per request</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

function UsageSkeleton() {
  return (
    <div className="space-y-6">
      <div>
        <Skeleton className="h-8 w-40" />
        <Skeleton className="h-4 w-64 mt-2" />
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Card key={i}>
            <CardHeader>
              <Skeleton className="h-4 w-24" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-8 w-16" />
              <Skeleton className="h-3 w-20 mt-1" />
            </CardContent>
          </Card>
        ))}
      </div>
      
      <Card>
        <CardHeader>
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-4 w-64" />
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="flex justify-between">
                <Skeleton className="h-4 w-16" />
                <Skeleton className="h-4 w-20" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}