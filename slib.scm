;"guile.init" Configuration file for SLIB for GUILE	-*-scheme-*-
;;; Author: Aubrey Jaffer
;;;
;;; This code is in the public domain.

(define-module (ice-9 slib))	; :no-backtrace
(define slib-module (current-module))

(define base:define define)
(define define
  (procedure->memoizing-macro
   (lambda (exp env)
     (cons (if (= 1 (length env)) 'define-public 'base:define) (cdr exp)))))

;;; Hack to make syncase macros work in the slib module
(if (nested-ref the-root-module '(app modules ice-9 syncase))
    (set-object-property! (module-local-variable (current-module) 'define)
			  '*sc-expander*
			  '(define)))

;;; (software-type) should be set to the generic operating system type.
;;; UNIX, VMS, MACOS, AMIGA and MS-DOS are supported.
(define software-type
  (if (string<? (version) "1.6")
      (lambda () 'UNIX)
      (lambda () 'unix)))

;;; (scheme-implementation-type) should return the name of the scheme
;;; implementation loading this file.
(define (scheme-implementation-type) 'guile)

;;; (scheme-implementation-home-page) should return a (string) URI
;;; (Uniform Resource Identifier) for this scheme implementation's home
;;; page; or false if there isn't one.
(define (scheme-implementation-home-page)
  "http://www.gnu.org/software/guile/guile.html")

;;; (scheme-implementation-version) should return a string describing
;;; the version the scheme implementation loading this file.
(define scheme-implementation-version version)

;;; (implementation-vicinity) should be defined to be the pathname of
;;; the directory where any auxillary files to your Scheme
;;; implementation reside.
(define implementation-vicinity
  (let* ((path (or (%search-load-path "ice-9/q.scm")
		   (error "Could not find ice-9/q.scm in " %load-path)))
	 (vic (substring path 0 (- (string-length path) 11))))
    (lambda () vic)))

;;; (library-vicinity) should be defined to be the pathname of the
;;; directory where files of Scheme library functions reside.
(define library-vicinity
  (let ((library-path
	 (or
	  ;; Use this getenv if your implementation supports it.
	  (and (defined? 'getenv) (getenv "SCHEME_LIBRARY_PATH"))
	  ;; Use this path if your scheme does not support GETENV
	  ;; or if SCHEME_LIBRARY_PATH is not set.
	  "/usr/share/guile/slib/"
	  (in-vicinity (implementation-vicinity) "slib/"))))
    (lambda () library-path)))

;;; (home-vicinity) should return the vicinity of the user's HOME
;;; directory, the directory which typically contains files which
;;; customize a computer environment for a user.
(define (home-vicinity)
  (let ((home (and (defined? 'getenv) (getenv "HOME"))))
    (and home
	 (case (software-type)
	   ((unix coherent ms-dos)	;V7 unix has a / on HOME
	    (if (eqv? #\/ (string-ref home (+ -1 (string-length home))))
		home
		(string-append home "/")))
	   (else home)))))
;@
(define (user-vicinity)
  (case (software-type)
    ((vms)	"[.]")
    (else	"")))
;@
(define vicinity:suffix?
  (let ((suffi
	 (case (software-type)
	   ((amiga)				'(#\: #\/))
	   ((macos thinkc)			'(#\:))
	   ((ms-dos windows atarist os/2)	'(#\\ #\/))
	   ((nosve)				'(#\: #\.))
	   ((unix coherent plan9)		'(#\/))
	   ((vms)				'(#\: #\]))
	   (else
	    (warn "require.scm" 'unknown 'software-type (software-type))
	    "/"))))
    (lambda (chr) (and (memv chr suffi) #t))))
;@
(define (pathname->vicinity pathname)
  (let loop ((i (- (string-length pathname) 1)))
    (cond ((negative? i) "")
	  ((vicinity:suffix? (string-ref pathname i))
	   (substring pathname 0 (+ i 1)))
	  (else (loop (- i 1))))))
;@
(define (program-vicinity)
  (define clp (current-load-port))
  (if clp
      (pathname->vicinity (port-filename clp))
      (slib:error 'program-vicinity " called; use slib:load to load")))
;@
(define sub-vicinity
  (case (software-type)
    ((vms) (lambda
	       (vic name)
	     (let ((l (string-length vic)))
	       (if (or (zero? (string-length vic))
		       (not (char=? #\] (string-ref vic (- l 1)))))
		   (string-append vic "[" name "]")
		   (string-append (substring vic 0 (- l 1))
				  "." name "]")))))
    (else (let ((*vicinity-suffix*
		 (case (software-type)
		   ((nosve) ".")
		   ((macos thinkc) ":")
		   ((ms-dos windows atarist os/2) "\\")
		   ((unix coherent plan9 amiga) "/"))))
	    (lambda (vic name)
	      (string-append vic name *vicinity-suffix*))))))
;@
(define (make-vicinity <pathname>) <pathname>)
;@
(define with-load-pathname
  (let ((exchange
	 (lambda (new)
	   (let ((old program-vicinity))
	     (set! program-vicinity new)
	     old))))
    (lambda (path thunk)
      (define old #f)
      (define vic (pathname->vicinity path))
      (dynamic-wind
	  (lambda () (set! old (exchange (lambda () vic))))
	  thunk
	  (lambda () (exchange old))))))

;;@ SLIB:FEATURES is a list of symbols naming the (SLIB) features
;;; initially supported by this implementation.
(define slib:features
  (append
      '(
	source				;can load scheme source files
					;(SLIB:LOAD-SOURCE "filename")
;;;	compiled			;can load compiled files
					;(SLIB:LOAD-COMPILED "filename")
	vicinity
	srfi-59

		       ;; Scheme report features
   ;; R5RS-compliant implementations should provide all 9 features.

;;;	r5rs				;conforms to
	eval				;R5RS two-argument eval
	values				;R5RS multiple values
	dynamic-wind			;R5RS dynamic-wind
;;;	macro				;R5RS high level macros
	delay				;has DELAY and FORCE
	multiarg-apply			;APPLY can take more than 2 args.
;;;	char-ready?
	rev4-optional-procedures	;LIST-TAIL, STRING-COPY,
					;STRING-FILL!, and VECTOR-FILL!

      ;; These four features are optional in both R4RS and R5RS

	multiarg/and-			;/ and - can take more than 2 args.
;;;	rationalize
;;;	transcript			;TRANSCRIPT-ON and TRANSCRIPT-OFF
	with-file			;has WITH-INPUT-FROM-FILE and
					;WITH-OUTPUT-TO-FILE

;;;	r4rs				;conforms to

;;;	ieee-p1178			;conforms to

;;;	r3rs				;conforms to

	rev2-procedures			;SUBSTRING-MOVE-LEFT!,
					;SUBSTRING-MOVE-RIGHT!,
					;SUBSTRING-FILL!,
					;STRING-NULL?, APPEND!, 1+,
					;-1+, <?, <=?, =?, >?, >=?
;;;	object-hash			;has OBJECT-HASH
	hash				;HASH, HASHV, HASHQ

	full-continuation		;can return multiple times
;;;	ieee-floating-point		;conforms to IEEE Standard 754-1985
					;IEEE Standard for Binary
					;Floating-Point Arithmetic.

			;; Other common features

;;;	srfi				;srfi-0, COND-EXPAND finds all srfi-*
;;;	sicp				;runs code from Structure and
					;Interpretation of Computer
					;Programs by Abelson and Sussman.
	defmacro			;has Common Lisp DEFMACRO
;;;	record				;has user defined data structures
	string-port			;has CALL-WITH-INPUT-STRING and
					;CALL-WITH-OUTPUT-STRING
	line-i/o
;;;	sort
;;;	pretty-print
;;;	object->string
;;;	format				;Common-lisp output formatting
;;;	trace				;has macros: TRACE and UNTRACE
;;;	compiler			;has (COMPILER)
;;;	ed				;(ED) is editor
	system				;posix (system <string>)
;;;	getenv				;posix (getenv <string>)
;;;	program-arguments		;returns list of strings (argv)
;;;	current-time			;returns time in seconds since 1/1/1970

		  ;; Implementation Specific features

	logical
	random				;Random numbers

	array
	array-for-each
	)

	(if (defined? 'getenv)
	    '(getenv)
	    '())

	(if (defined? 'current-time)
	    '(current-time)
	    '())

	(if (defined? 'char-ready?)
	    '(char-ready?)
	    '())))

;;; (OUTPUT-PORT-WIDTH <port>)
(define (output-port-width . arg) 79)

;;; (OUTPUT-PORT-HEIGHT <port>)
(define (output-port-height . arg) 24)

;;; (CURRENT-ERROR-PORT)
;;(define current-error-port
;;  (let ((port (current-output-port)))
;;    (lambda () port)))

;; If the program is killed by a signal, /bin/sh normally gives an
;; exit code of 128+signum.  If /bin/sh itself is killed by a signal
;; then we do the same 128+signum here.
;;
;; "status:stop-sig" shouldn't arise here, since system shouldn't be
;; calling waitpid with WUNTRACED, but allow for it anyway, just in
;; case.
(set! system
      (let ((guile-core-system system))
	(lambda (str)
	  (define st (guile-core-system str))
	  (or (status:exit-val st)
	      (+ 128 (or (status:term-sig st)
			 (status:stop-sig st)))))))

;;; for line-i/o
(use-modules (ice-9 popen))
(define (system->line command . tmp)
  (let ((ipip (open-input-pipe command)))
    (define line (read-line ipip))
    (let ((status (close-pipe ipip)))
      (and (or (eqv? 0 (status:exit-val status))
	       (status:term-sig status)
	       (status:stop-sig status))
	   (if (eof-object? line) "" line)))))
;; rdelim was loaded by default in guile 1.6, but not in 1.8
;; load it to get read-line, read-line! and write-line,
;; and re-export them for the benefit of loading this file from (ice-9 slib)
(cond ((string>=? (scheme-implementation-version) "1.8")
       (use-modules (ice-9 rdelim))
       (re-export read-line)
       (re-export read-line!)
       (re-export write-line)))

(set! delete-file
      (let ((guile-core-delete-file delete-file))
	(lambda (filename)
	  (catch 'system-error
		 (lambda () (guile-core-delete-file filename) #t)
		 (lambda args #f)))))

;;; FORCE-OUTPUT flushes any pending output on optional arg output port
;;; use this definition if your system doesn't have such a procedure.
;;(define (force-output . arg) #t)

;;; CALL-WITH-INPUT-STRING and CALL-WITH-OUTPUT-STRING are the string
;;; port versions of CALL-WITH-*PUT-FILE.

(define (make-exchanger obj)
  (lambda (rep) (let ((old obj)) (set! obj rep) old)))
(set! open-file
      (let ((guile-core-open-file open-file))
	(lambda (filename modes)
	  (guile-core-open-file filename
				(if (symbol? modes)
				    (symbol->string modes)
				    modes)))))
(define (call-with-open-ports . ports)
  (define proc (car ports))
  (cond ((procedure? proc) (set! ports (cdr ports)))
	(else (set! ports (reverse ports))
	      (set! proc (car ports))
	      (set! ports (reverse (cdr ports)))))
  (let ((ans (apply proc ports)))
    (for-each close-port ports)
    ans))

(if (not (defined? 'browse-url))
    ;; Nothing special to do for this, so straight from
    ;; Template.scm.  Maybe "sensible-browser" for a debian
    ;; system would be worth trying too (and would be good on a
    ;; tty).
    (define (browse-url url)
      (define (try cmd end) (zero? (system (string-append cmd url end))))
      (or (try "netscape-remote -remote 'openURL(" ")'")
	  (try "netscape -remote 'openURL(" ")'")
	  (try "netscape '" "'&")
	  (try "netscape '" "'"))))

;;; "rationalize" adjunct procedures.
;;(define (find-ratio x e)
;;  (let ((rat (rationalize x e)))
;;    (list (numerator rat) (denominator rat))))
;;(define (find-ratio-between x y)
;;  (find-ratio (/ (+ x y) 2) (/ (- x y) 2)))

;;; CHAR-CODE-LIMIT is one greater than the largest integer which can
;;; be returned by CHAR->INTEGER.
;; In Guile-1.8.0: (string>? (string #\000) (string #\200)) ==> #t
(if (string=? (version) "1.8.0")
    (define char-code-limit 128))

;;; MOST-POSITIVE-FIXNUM is used in modular.scm
;;(define most-positive-fixnum #x0FFFFFFF)

;;; SLIB:EVAL is single argument eval using the top-level (user) environment.
(define slib:eval
  (if (string<? (scheme-implementation-version) "1.5")
      eval
      (let ((ie (interaction-environment)))
	(lambda (expression)
	  (eval expression ie)))))
;; slib:eval-load definition moved to "require.scm"

;;; Define SLIB:EXIT to be the implementation procedure to exit or
;;; return if exiting not supported.
(define slib:exit quit)

;;; Here for backward compatability
;;(define scheme-file-suffix
;;  (let ((suffix (case (software-type)
;;		  ((nosve) "_scm")
;;		  (else ".scm"))))
;;    (lambda () suffix)))

;;; (define (guile:wrap-case-insensitive proc)
;;;   (lambda args
;;;     (save-module-excursion
;;;      (lambda ()
;;;        (set-current-module slib-module)
;;;        (let ((old (read-options)))
;;; 	 (dynamic-wind
;;; 	     (lambda () (read-enable 'case-insensitive))
;;; 	     (lambda () (apply proc args))
;;; 	     (lambda () (read-options old))))))))

;;; (define read (guile:wrap-case-insensitive read))

;;; (SLIB:LOAD-SOURCE "foo") should load "foo.scm" or with whatever
;;; suffix all the module files in SLIB have.  See feature 'SOURCE.
;;; (define slib:load
;;;   (let ((load-file (guile:wrap-case-insensitive load)))
;;;     (lambda (<pathname>)
;;;       (load-file (string-append <pathname> (scheme-file-suffix))))))
(define (slib:load-helper loader)
  (lambda (name)
    (save-module-excursion
     (lambda ()
       (set-current-module slib-module)
       (let ((errinfo (catch 'system-error
			     (lambda () (loader name) #f)
			     (lambda args args))))
	 (if (and errinfo
		  (catch 'system-error
			 (lambda () (loader (string-append name ".scm")) #f)
			 (lambda args args)))
	     (apply throw errinfo)))))))
(define slib:load (slib:load-helper load))
(define slib:load-from-path (slib:load-helper load-from-path))

(define slib:load-source slib:load)

;;; (SLIB:LOAD-COMPILED "foo") should load the file that was produced
;;; by compiling "foo.scm" if this implementation can compile files.
;;; See feature 'COMPILED.
(define slib:load-compiled slib:load)

(define defmacro:eval slib:eval)
(define defmacro:load slib:load)

(define (defmacro:expand* x)
  (require 'defmacroexpand) (apply defmacro:expand* x '()))

;;; If your implementation provides R4RS macros:
(define macro:eval slib:eval)
(define macro:load slib:load)

(define slib:warn warn)
(define slib:error error)

;;; define these as appropriate for your system.
(define slib:tab #\tab)
(define slib:form-feed #\page)

;;; {Time}
(define difftime -)
(define offset-time +)

;;; Early version of 'logical is built-in
(define (copy-bit index to bool)
  (if bool
      (logior to (arithmetic-shift 1 index))
      (logand to (lognot (arithmetic-shift 1 index)))))
(define (bit-field n start end)
  (logand (- (expt 2 (- end start)) 1)
	  (arithmetic-shift n (- start))))
(define (bitwise-if mask n0 n1)
  (logior (logand mask n0)
	  (logand (lognot mask) n1)))
(define (copy-bit-field to from start end)
  (bitwise-if (arithmetic-shift (lognot (ash -1 (- end start))) start)
	      (arithmetic-shift from start)
	      to))
(define (rotate-bit-field n count start end)
  (define width (- end start))
  (set! count (modulo count width))
  (let ((mask (lognot (ash -1 width))))
    (define azn (logand mask (arithmetic-shift n (- start))))
    (logior (arithmetic-shift
	     (logior (logand mask (arithmetic-shift azn count))
		     (arithmetic-shift azn (- count width)))
	     start)
	    (logand (lognot (ash mask start)) n))))
(define (log2-binary-factors n)
  (+ -1 (integer-length (logand n (- n)))))
(define (bit-reverse k n)
  (do ((m (if (negative? n) (lognot n) n) (arithmetic-shift m -1))
       (k (+ -1 k) (+ -1 k))
       (rvs 0 (logior (arithmetic-shift rvs 1) (logand 1 m))))
      ((negative? k) (if (negative? n) (lognot rvs) rvs))))
(define (reverse-bit-field n start end)
  (define width (- end start))
  (let ((mask (lognot (ash -1 width))))
    (define zn (logand mask (arithmetic-shift n (- start))))
    (logior (arithmetic-shift (bit-reverse width zn) start)
	    (logand (lognot (ash mask start)) n))))

(define (integer->list k . len)
  (if (null? len)
      (do ((k k (arithmetic-shift k -1))
	   (lst '() (cons (odd? k) lst)))
	  ((<= k 0) lst))
      (do ((idx (+ -1 (car len)) (+ -1 idx))
	   (k k (arithmetic-shift k -1))
	   (lst '() (cons (odd? k) lst)))
	  ((negative? idx) lst))))
(define (list->integer bools)
  (do ((bs bools (cdr bs))
       (acc 0 (+ acc acc (if (car bs) 1 0))))
      ((null? bs) acc)))
(define (booleans->integer . bools)
  (list->integer bools))

;;;; SRFI-60 aliases
(define arithmetic-shift ash)
(define bitwise-ior logior)
(define bitwise-xor logxor)
(define bitwise-and logand)
(define bitwise-not lognot)
;;(define bit-count logcount)
(define bit-set?   logbit?)
(define any-bits-set? logtest)
(define first-set-bit log2-binary-factors)
(define bitwise-merge bitwise-if)

;;; array-for-each
(define (array-indexes ra)
  (let ((ra0 (apply make-array '#() (array-shape ra))))
    (array-index-map! ra0 list)
    ra0))
(define (array:copy! dest source)
  (array-map! dest identity source))
(define (array-null? array)
  (zero? (apply * (map (lambda (bnd) (- 1 (apply - bnd)))
		       (array-shape array)))))
;; DIMENSIONS->UNIFORM-ARRAY and list->uniform-array in Guile-1.6.4
;; cannot make empty arrays.
(set! make-array
      (lambda (prot . args)
	(if (array-null? prot)
	    (dimensions->uniform-array args (array-prototype prot))
	    (dimensions->uniform-array args (array-prototype prot)
				       (apply array-ref prot
					      (map car (array-shape prot)))))))
(define create-array make-array)
(define (make-uniform-wrapper prot)
  (if (string? prot) (set! prot (string->number prot)))
  (if prot
      (if (string<? (version) "1.8")
	  (lambda opt (if (null? opt)
			  (list->uniform-array 1 prot (list prot))
			  (list->uniform-array 0 prot opt)))
	  (lambda opt (if (null? opt)
			  (list->uniform-array 1 prot (list prot))
			  (list->uniform-array 0 prot (car opt)))))
      vector))
(define ac64 (make-uniform-wrapper "+i"))
(define ac32 ac64)
(define ar64 (make-uniform-wrapper "1/3"))
(define ar32 (make-uniform-wrapper "1."))
(define as64 vector)
(define as32 (make-uniform-wrapper -32))
(define as16 as32)
(define as8  as32)
(define au64 vector)
(define au32 (make-uniform-wrapper  32))
(define au16 au32)
(define au8  au32)
(define at1  (make-uniform-wrapper  #t))

;;; New SRFI-58 names
;; flonums
(define A:floC128b ac64)
(define A:floC64b ac64)
(define A:floC32b ac32)
(define A:floC16b ac32)
(define A:floR128b ar64)
(define A:floR64b ar64)
(define A:floR32b ar32)
(define A:floR16b ar32)
;; decimal flonums
(define A:floR128d ar64)
(define A:floR64d ar64)
(define A:floR32d ar32)
;; fixnums
(define A:fixZ64b as64)
(define A:fixZ32b as32)
(define A:fixZ16b as16)
(define A:fixZ8b  as8)
(define A:fixN64b au64)
(define A:fixN32b au32)
(define A:fixN16b au16)
(define A:fixN8b  au8)
(define A:bool    at1)

;;; And case-insensitive versions
;; flonums
(define a:floc128b ac64)
(define a:floc64b ac64)
(define a:floc32b ac32)
(define a:floc16b ac32)
(define a:flor128b ar64)
(define a:flor64b ar64)
(define a:flor32b ar32)
(define a:flor16b ar32)
;; decimal flonums
(define a:flor128d ar64)
(define a:flor64d ar64)
(define a:flor32d ar32)
;; fixnums
(define a:fixz64b as64)
(define a:fixz32b as32)
(define a:fixz16b as16)
(define a:fixz8b  as8)
(define a:fixn64b au64)
(define a:fixn32b au32)
(define a:fixn16b au16)
(define a:fixn8b  au8)
(define a:bool    at1)

;;; {Random numbers}
(define (make-random-state . args)
  (let ((seed (if (null? args) *random-state* (car args))))
    (cond ((string? seed))
	  ((number? seed) (set! seed (number->string seed)))
	  (else (let ()
		  (require 'object->string)
		  (set! seed (object->limited-string seed 50)))))
    (seed->random-state seed)))
(if (not (defined? 'random:chunk))
    (define (random:chunk sta) (random 256 sta)))

;;; Support for older versions of Scheme.  Not enough code for its own file.
;;(define (last-pair l) (if (pair? (cdr l)) (last-pair (cdr l)) l))

(define t #t)
(define nil #f)

;;; rev2-procedures
(define <? <)
(define <=? <=)
(define =? =)
(define >? >)
(define >=? >=)

(slib:load (in-vicinity (library-vicinity) "require"))
