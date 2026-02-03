import { createSlice } from '@reduxjs/toolkit';
import {type User} from "./userApi.ts";



interface UserState {
    user: User | null;
}

const userSlice = createSlice({
    name: 'user',
    initialState: {
        user: null
    } as UserState,
    reducers: {},
});

export default userSlice.reducer;
