import { atom } from 'jotai';

import type { Project } from '@/api/projects';

export const useProjectsStore = atom<Project[]>([]);
