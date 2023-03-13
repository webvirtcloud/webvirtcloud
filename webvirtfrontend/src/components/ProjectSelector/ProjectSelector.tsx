import { useAtom, useAtomValue } from 'jotai';
import { useEffect, useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import tw, { css } from 'twin.macro';

import type { Project } from '@/api/projects';
import { Button } from '@/components/Button';
import { CheckCircle, ChevronUpDown } from '@/components/Icons';
import { useOnClickOutside } from '@/hooks/useOnClickOutside';
import { useProjectStore } from '@/store/project';
import { useProjectsStore } from '@/store/projects';

const ProjectSelector = (): JSX.Element => {
  const ref = useRef<HTMLDivElement>(null);
  const [isOpen, toggle] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const projects = useAtomValue(useProjectsStore);
  const [project, setProject] = useAtom(useProjectStore);

  const handleProjectSelect = (project: Project) => {
    setProject(project);
    navigate(`/projects/${project.uuid}`);
  };

  useEffect(() => {
    if (isOpen) {
      toggle(false);
    }
  }, [location]);

  useOnClickOutside(ref, () => toggle(false));

  return (
    <div css={tw`relative min-w-[132px]`} ref={ref}>
      <div css={tw`flex items-center justify-between w-full text-left`}>
        <Link
          to={`/projects/${project?.uuid}/servers`}
          css={tw`flex items-center h-6 px-2 transition-colors rounded-md hover:bg-interactive-hover`}
        >
          <div css={tw`min-w-0 overflow-hidden`}>
            <h4 css={tw`font-bold`}>{project?.name}</h4>
          </div>
        </Link>

        <button
          onClick={() => toggle(!isOpen)}
          type="button"
          css={tw`h-6 px-1 transition-colors rounded-md hover:bg-interactive-hover`}
        >
          <ChevronUpDown width={16} height={16} />
        </button>
      </div>
      {isOpen && (
        <div
          css={tw`min-w-[200px] bg-base absolute z-30 top-[calc(100% + 8px)] left-0 right-0 shadow-md ring-1 ring-black/5 rounded-md p-2`}
        >
          {projects && (
            <ul css={tw`mb-2`}>
              {projects.map((item) => (
                <li key={item.uuid}>
                  <button
                    onClick={() => handleProjectSelect(item)}
                    css={tw`flex items-center justify-between w-full p-2 space-x-2 text-left rounded hover:bg-interactive-hover`}
                  >
                    <span css={tw`flex flex-1 space-x-2`}>
                      {/* <span
                        css={[
                          css({ backgroundColor: item.color_hex }),
                          tw`flex-shrink-0 w-5 h-5 rounded`,
                        ]}
                      ></span> */}
                      <span css={[project?.uuid === item.uuid && tw`font-bold`]}>
                        {item.name}
                      </span>
                    </span>
                    {project?.uuid === item.uuid && (
                      <span css={tw`flex-shrink-0 w-5 h-5 text-green-500`}>
                        <CheckCircle />
                      </span>
                    )}
                  </button>
                </li>
              ))}
            </ul>
          )}
          <Button
            onClick={() => navigate('/projects/create')}
            css={tw`w-full`}
            type="button"
            size="lg"
          >
            Create project
          </Button>
        </div>
      )}
    </div>
  );
};

export default ProjectSelector;
