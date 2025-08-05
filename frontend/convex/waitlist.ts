import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const addToWaitlist = mutation({
  args: { email: v.string() },
  handler: async (ctx, args) => {
    // Check if email already exists
    const existingEntry = await ctx.db
      .query("waitlist")
      .withIndex("by_email", (q) => q.eq("email", args.email))
      .unique();

    if (existingEntry) {
      throw new Error("Email already registered on waitlist");
    }

    // Add to waitlist
    const id = await ctx.db.insert("waitlist", {
      email: args.email,
      createdAt: Date.now(),
    });

    return { 
      success: true, 
      message: "Successfully added to waitlist!", 
      id 
    };
  },
});

export const getWaitlistCount = query({
  args: {},
  handler: async (ctx) => {
    const count = await ctx.db.query("waitlist").collect().then(entries => entries.length);
    return count;
  },
});