import request from './fetch';

export type Server = {
  uuid: string;
  name: string;
  size: {
    name: string;
    vcpu: number;
    memory: number;
    storage: number;
  };
  distribution: {
    name: string;
  };
  status: 'active' | 'inactive';
  created_at: string;
  tags: string[];
  project_uuid: string;
  region: {
    slug: string;
    name: string;
  };
  network: {
    ipv4: [{ type: 'public' | 'private'; address: string }];
  };
};

const servers: Server[] = [
  {
    uuid: '111111111',
    name: 'ubuntu-18.04',
    size: {
      name: '1gb-1vpcu-32gb',
      memory: 1,
      storage: 32,
      vcpu: 1,
    },
    distribution: { name: 'Ubuntu' },
    status: 'active',
    created_at: '2022-11-06T05:44:51.334101Z',
    tags: [],
    project_uuid: '111-aaa-222-bbb',
    region: {
      slug: 'fra',
      name: 'Frankfurt',
    },
    network: {
      ipv4: [{ type: 'public', address: '50.70.102.10' }],
    },
  },
  {
    uuid: '222222222',
    name: 'ubuntu-18.04',
    size: {
      name: '1gb-1vpcu-32gb',
      memory: 1,
      storage: 32,
      vcpu: 1,
    },
    distribution: { name: 'Ubuntu' },
    status: 'inactive',
    created_at: '2022-11-06T05:44:51.334101Z',
    tags: ['ubuntu'],
    project_uuid: '111-aaa-222-bbb',
    region: {
      slug: 'fra',
      name: 'Frankfurt',
    },
    network: {
      ipv4: [{ type: 'public', address: '50.70.102.10' }],
    },
  },
  {
    uuid: '3333333333',
    name: 'Fedora-32.02',
    size: {
      name: '1gb-1vpcu-32gb',
      memory: 1,
      storage: 32,
      vcpu: 1,
    },
    distribution: { name: 'Fedora' },
    status: 'active',
    created_at: '2022-11-06T05:44:51.334101Z',
    tags: [],
    project_uuid: '333-ccc-444-ddd',
    region: {
      slug: 'fra',
      name: 'Frankfurt',
    },
    network: {
      ipv4: [{ type: 'public', address: '50.70.102.10' }],
    },
  },
  {
    uuid: '4444444444',
    name: 'Fedora-32.02',
    size: {
      name: '1gb-1vpcu-32gb',
      memory: 1,
      storage: 32,
      vcpu: 1,
    },
    distribution: { name: 'Fedora' },
    status: 'active',
    created_at: '2022-11-06T05:44:51.334101Z',
    tags: ['ubuntu'],
    project_uuid: '333-ccc-444-ddd',
    region: {
      slug: 'fra',
      name: 'Frankfurt',
    },
    network: {
      ipv4: [{ type: 'public', address: '50.70.102.10' }],
    },
  },
  {
    uuid: '555555555',
    name: 'Fedora-32.02',
    size: {
      name: '1gb-1vpcu-32gb',
      memory: 1,
      storage: 32,
      vcpu: 1,
    },
    distribution: { name: 'Fedora' },
    status: 'inactive',
    created_at: '2022-11-06T05:44:51.334101Z',
    tags: [],
    project_uuid: '333-ccc-444-ddd',
    region: {
      slug: 'fra',
      name: 'Frankfurt',
    },
    network: {
      ipv4: [{ type: 'public', address: '50.70.102.10' }],
    },
  },
  {
    uuid: '66666666',
    name: 'ubuntu-18.04',
    size: {
      name: '1gb-1vpcu-32gb',
      memory: 1,
      storage: 32,
      vcpu: 1,
    },
    distribution: { name: 'Ubuntu' },
    status: 'inactive',
    created_at: '2022-11-06T05:44:51.334101Z',
    tags: [],
    project_uuid: '333-ccc-444-ddd',
    region: {
      slug: 'fra',
      name: 'Frankfurt',
    },
    network: {
      ipv4: [{ type: 'public', address: '50.70.102.10' }],
    },
  },
];

export const getServers = (): Promise<{ servers: Server[] }> => {
  return new Promise((resolve) => {
    setTimeout(
      () =>
        resolve({
          servers: servers,
        }),
      500,
    );
  });
  // return request.get('/servers').json();
};

export const getServer = (uuid: string): Promise<{ server: Server }> => {
  return new Promise((resolve) => {
    setTimeout(
      () => resolve({ server: servers.find((server) => server.uuid === uuid) }),
      500,
    );
  });
  // return request.get('/server').json();
};
