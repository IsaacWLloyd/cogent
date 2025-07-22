import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { FileText, Search, Bot } from "lucide-react"

export default function Features() {
  const features = [
    {
      icon: <FileText className="h-8 w-8" />,
      title: "Auto Documentation",
      description: "Automatically generates comprehensive documentation for every file you create or modify."
    },
    {
      icon: <Search className="h-8 w-8" />,
      title: "Intelligent Search",
      description: "Hybrid search using full-text and vector embeddings to find relevant context instantly."
    },
    {
      icon: <Bot className="h-8 w-8" />,
      title: "Claude Code Integration",
      description: "Seamlessly integrates with Claude Code via MCP protocol for enhanced AI-assisted development."
    }
  ]

  return (
    <section className="py-20 bg-secondary/50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold mb-4 text-foreground">
            Powerful Features
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            COGENT provides essential tools to keep your codebase documented and organized.
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="bg-card border-border">
              <CardHeader>
                <div className="mb-4 text-primary">
                  {feature.icon}
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
                <CardDescription className="text-muted-foreground">
                  {feature.description}
                </CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}