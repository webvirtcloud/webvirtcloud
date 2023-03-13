import request from './fetch';

export type Project = {
  uuid: string;
  color_hex: string;
  name: string;
  is_default: boolean;
  members: string[];
};

const projects: Project[] = [
  {
    uuid: '111-aaa-222-bbb',
    color_hex: '#89f',
    name: 'Basic',
    is_default: true,
    members: [],
  },
  {
    uuid: '333-ccc-444-ddd',
    color_hex: '#738',
    name: 'Frontend',
    is_default: false,
    members: [],
  },
  {
    uuid: '555-eee-666-fff',
    color_hex: '#45d',
    name: 'Backend',
    is_default: false,
    members: [],
  },
];

export const getProjects = (): Promise<{ projects: Project[] }> => {
  return new Promise((resolve) => {
    setTimeout(() => resolve({ projects }), 500);
  });
  // return request.get('projects').json();
};

export const getProject = (uuid: string): Promise<{ project: Project }> => {
  return new Promise((resolve) => {
    setTimeout(
      () => resolve({ project: projects.find((project) => project.uuid === uuid) }),
      500,
    );
  });
  // return request.get('/server').json();
};
