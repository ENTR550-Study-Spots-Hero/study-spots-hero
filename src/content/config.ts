import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
    type: 'content',
    // Type-check frontmatter using a schema
    schema: z.object({
        title: z.string(),
        description: z.string(),
        // Transform string to Date object
        pubDate: z.coerce.date(),
        updatedDate: z.coerce.date().optional(),
        heroImage: z.string().optional(),
    }),
});

const studySpotCollection = defineCollection({
    type: 'content',
    schema: z.object({
        building: z.string(),
        timestamp: z.coerce.date(),
        isQuiet: z.boolean(),
        isCollaborative: z.boolean(),
        caenAccess: z.boolean(),
        naturalLight: z.number(),
        comfortableTemp: z.number(),
        outletAvailability: z.number(),
        furnitureComfort: z.number(),
        restroomDistance: z.number(),
        reservable: z.boolean(),
        busyness: z.number(),
        title: z.string(),
    }),
});

export const collections = { blog, studySpotCollection };
