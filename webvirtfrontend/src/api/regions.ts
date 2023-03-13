import request from './fetch';

type Region = {
  available: boolean;
  features: string[];
  name: string;
  sizes: string[];
  slug: string;
};

export const getRegions = (): Promise<{ regions: Region[] }> => {
  return request.get('regions').json();
};
