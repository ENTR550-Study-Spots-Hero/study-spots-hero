import { defineCollection, z } from 'astro:content';

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

export const collections = { studySpotCollection };
