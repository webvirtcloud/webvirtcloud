import { useAtom, useSetAtom } from 'jotai';
import { useEffect } from 'react';
import { Navigate, Outlet, useLocation, useNavigate } from 'react-router-dom';
import tw from 'twin.macro';

import { getProfile } from '@/api/account';
// import { getProjects } from '@/api/projects';
import Navbar from '@/components/Navbar';
// import { PROJECT_UUID_LOCALSTORAGE_KEY } from '@/constants';
import { useProfileStore } from '@/store/profile';
// import { useProjectStore } from '@/store/project';
// import { useProjectsStore } from '@/store/projects';

const DefaultLayout = (): JSX.Element => {
  const setProfile = useSetAtom(useProfileStore);
  // const setProjects = useSetAtom(useProjectsStore);
  // const [project, setProject] = useAtom(useProjectStore);
  // const navigate = useNavigate();
  // const { pathname } = useLocation();
  const isAuthenticated = !!window.localStorage.getItem('token');

  // if (
  //   pathname === '/sign-in' ||
  //   pathname === '/sign-up' ||
  //   pathname === '/reset-password'
  // ) {
  //   return isAuthenticated ? <Navigate to="/" replace /> : <Outlet />;
  // }

  // if (!isAuthenticated) {
  //   return <Navigate to="/sign-in" replace />;
  // }

  const fetch = async () => {
    const response = await getProfile();

    //   const { projects } = await getProjects();

    //   const projectUuidFromLocalStorage = window.localStorage.getItem(
    //     PROJECT_UUID_LOCALSTORAGE_KEY,
    //   );

    //   const project = projectUuidFromLocalStorage
    //     ? projects.find((item) => item.uuid === projectUuidFromLocalStorage)
    //     : projects.find((item) => item.is_default);

    //   setProjects(projects);
    //   setProject(project);
    setProfile(response.profile);

    //   pathname === '/' && navigate({ pathname: `/projects/${project?.uuid}/servers` });
  };

  useEffect(() => {
    isAuthenticated && fetch().catch(console.error);
  }, []);

  // useEffect(() => {
  //   if (pathname === '/') {
  //     fetch().catch(console.error);
  //   }
  // }, [pathname]);

  // useEffect(() => {
  //   if (project) {
  //     window.localStorage.setItem(PROJECT_UUID_LOCALSTORAGE_KEY, project.uuid);
  //   }
  // }, [project]);

  return isAuthenticated ? (
    <main css={tw`flex flex-col min-h-screen`}>
      <Navbar />
      <div css={tw`container flex-1 px-4 py-8 mx-auto`}>
        <Outlet />
      </div>
    </main>
  ) : (
    <Navigate to="/sign-in" replace />
  );
};

export default DefaultLayout;
