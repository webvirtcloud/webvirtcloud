import { atom } from 'jotai';

import type { Profile } from '@/api/account';

export const useProfileStore = atom<undefined | Profile>(undefined);
