import { atom } from 'jotai';

import type { Project } from '@/api/projects';

export const useProjectStore = atom<undefined | Project>(undefined);
