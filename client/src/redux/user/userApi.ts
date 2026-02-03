import {apiSlice} from "../apiSlice.ts";

export type User = {
    id: string;
    name: string;
    email: string;
    createdAt?: string;
}

export const userApi = apiSlice.injectEndpoints({

    endpoints: () => ({
   

    }),

});


// export const {} = userApi;
