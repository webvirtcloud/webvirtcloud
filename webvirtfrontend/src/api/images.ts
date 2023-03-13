import request from './fetch';

type Image = {
  created_at: string;
  description: string;
  distribution: string;
  min_disk_size: number;
  name: string;
  public: true;
  regions: string[];
  size_gigabytes: number;
  slug: string;
  status: string;
  type: 'distribution';
};

export const getImages = (type: 'distribution'): Promise<{ images: Image[] }> => {
  return request.get(`images?type=${type}`).json();
};
