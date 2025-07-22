import { Button } from "@/components/ui/button"

export default function Hero() {
  return (
    <section className="py-20 lg:py-32 bg-background">
      <div className="container mx-auto text-center px-4">
        <h1 className="text-4xl lg:text-6xl font-bold mb-6 text-foreground">
          Code Organization and{" "}
          <span className="text-primary">Generation Enhancement</span> Tool
        </h1>
        <p className="text-lg lg:text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
          COGENT forces Claude Code to generate and maintain comprehensive documentation for every code file, 
          ensuring your codebase remains well-documented and understandable.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button size="lg" className="text-base">
            Get Started
          </Button>
          <Button variant="outline" size="lg" className="text-base">
            View Documentation
          </Button>
        </div>
      </div>
    </section>
  )
}