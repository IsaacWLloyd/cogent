import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

export default function CTA() {
  return (
    <section className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <Card className="max-w-4xl mx-auto bg-card border-border">
          <CardContent className="p-12 text-center">
            <h2 className="text-3xl lg:text-4xl font-bold mb-6 text-foreground">
              Ready to get started?
            </h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              Install COGENT in your project and start generating comprehensive documentation 
              automatically with every code change.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="text-base">
                Install COGENT
              </Button>
              <Button variant="outline" size="lg" className="text-base">
                View Documentation
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  )
}